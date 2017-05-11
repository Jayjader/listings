from secrets import token_urlsafe

from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.utils import timezone

from .models import Listing

placeholder = "\nThis is a placeholder page."
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


def contact(request, pk: int):
    # TODO: Form; inputs: message, subject & sender email
    # send_contact_email(extract_contact_message(request.post))
    return HttpResponse("Contact the creator of a certain listing." + placeholder)


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
    # TODO: Edit listing title, description
    return HttpResponse("Edit a listing." + placeholder)
