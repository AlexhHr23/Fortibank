from django.shortcuts import render
from django.http import HttpResponse


# def index(request):
#     return render(request, "userauths/sign-in.html")

def index(request):
    return render(request, "userauths/sign-in.html")

def contact(request):
    return render(request, "core/contact.html")

def about(request):
    return render(request, "core/about.html")

