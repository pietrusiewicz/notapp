from django.shortcuts import HttpResponse


def index(r):
    return HttpResponse("Hello World")
