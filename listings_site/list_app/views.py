from secrets import token_urlsafe

from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.utils import timezone

from .models import Listing

DEBUG_NEW = True


def index(request):
    latest_listings = Listing.objects.order_by('-last_edit_date')
    context = {'latest_listings': latest_listings}
    template = 'list_app/index.html'
    return render(request, template, context)


def detail(request, pk: int):
    listing = get_object_or_404(Listing, pk=pk)
    url = reverse('list_app:contact', args=(pk,))
    context = {'listing': listing, 'contact_url': url}
    template = 'list_app/detail.html'
    return render(request, template, context)


def send_contact_email(address: str, subject: str, message: str, listing: Listing):
    sender_email = address

    new_message = '''
    Someone has sent you a message concerning your post "{title}" on Listings!\n
    Here's their message:\n
    {subject}\n
    {message}\n\n
    They have provided this email to contact them at: {sender}
    '''.format(sender=sender_email, title=listing.title, subject=subject, message=message)

    send_mail(subject='Message about your listing {}'.format(listing.title),
              message=new_message,
              from_email='donotreply@listings.com',
              recipient_list=[listing.creator_email])


def extract_contact_message(post):
    return post['sender_email'], post['subject'], post['message']


def contact(request, pk: int):
    listing = get_object_or_404(Listing, pk=pk)
    template = 'list_app/contact.html'
    listing_url = reverse('list_app:detail', args=(listing.id,))
    context = {'listing_title': listing.title, 'listing_url': listing_url}

    if request.method == 'GET':
        return render(request, template, context)

    elif request.method == 'POST':
        # "relay" the message posted
        send_contact_email(*extract_contact_message(request.POST), listing)

        # tell the template that the email was sent correctly so that it notifies the user
        context['posted'] = True
        return HttpResponseRedirect('', loader.get_template(template).render(context, request))


def generate_guaranteed_unique_token():
    # Recursively generate a token until a unique one is had (should
    # not go more than 2 layers deep given the scale of this app)
    token = token_urlsafe()
    collisions = Listing.objects.filter(edit_token=token)
    if len(collisions) > 0:
        return generate_guaranteed_unique_token()
    else:
        return token


def send_creation_email(email: str, token: str):
    message = 'Thanks for using Listings!\nTo edit your listing, go to this link: {domain}/edit/{token}'
    send_mail(subject='New Listing',
              message=message.format(domain='localhost:8000/listings' if DEBUG_NEW else 'listings.com',
                                     token=token),
              from_email='donotreply@listings.com',
              recipient_list=[email])


def new(request):
    template = loader.get_template('list_app/new.html')
    context = {}

    if request.method == 'POST':
        # try to save new listing, generate edit link/token & send it to the creator
        title = request.POST['title']
        description = request.POST['description']
        email = request.POST['creator email']
        token = generate_guaranteed_unique_token()
        Listing.objects.create(title=title,
                               description=description,
                               creator_email=email,
                               edit_token=token,
                               last_edit_date=timezone.now())
        context['posted'] = True
        send_creation_email(email, token)
        return HttpResponseRedirect('', template.render(context, request))
    else:
        return HttpResponse(template.render(context, request))


def edit_listing(request, token: str):
    listing = get_object_or_404(Listing, edit_token=token)
    template = 'list_app/edit.html'
    context = {'listing': listing}

    if request.method == 'GET':
        # display the listing attributes' current values
        return render(request, template, context)

    elif request.method == 'POST':
        # first, determine if we're supposed to update the values, or delete the listing
        if 'save' in request.POST:
            listing.title = request.POST['title']
            listing.description = request.POST['description']
            listing.creator_email = request.POST['creator email']
            listing.last_edit_date = timezone.now()
            listing.save()

            # alert the template that an edit was saved
            context['saved'] = True
            return HttpResponseRedirect('', loader.get_template(template).render(context, request))

        elif 'delete' in request.POST:
            listing.delete()
            return HttpResponseRedirect(reverse('list_app:index'))
