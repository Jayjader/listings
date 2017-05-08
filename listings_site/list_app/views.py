from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from secrets import token_urlsafe

from .models import Listing

placeholder = "\nThis is a placeholder page."


def index(request):
    latest_listings = Listing.objects.order_by('-last_edit_date')[:10]
    template = loader.get_template('list_app/index.html')
    context = {'latest_listings': latest_listings}
    return HttpResponse(template.render(context, request))


def detail(request, pk: int):
    return HttpResponse("Here are the details for a particular listing." + "\ntested: " + str(pk) + placeholder)


def contact(request, pk: int):
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
    message = 'Thanks for using Listings!\nTo edit your listing, go to this link: listings.com/edit/{}'
    send_mail(subject='New Listing',
              message=message.format(token),
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

    return HttpResponse(template.render(context, request))


def edit_listing(request, token: str):
    return HttpResponse("Edit a listing." + placeholder)
