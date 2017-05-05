from django.shortcuts import render
from django.http import HttpResponse

placeholder = "\nThis is a placeholder page."


def index(request):
    return HttpResponse("Welcome to listings!" + placeholder)


def detail(request, pk: int):
    return HttpResponse("Here are the details for a particular listing." + placeholder)


def contact(request, pk: int):
    return HttpResponse("Contact the creator of a certain listing." + placeholder)


def create_listing(request):
    return HttpResponse("Post a new listing." + placeholder)


def edit_listing(request, pk: int):
    return HttpResponse("Edit a listing." + placeholder)
