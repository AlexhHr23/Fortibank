from django.shortcuts import render
from django.http import HttpResponse

def burito(request):
    return render(request, "core/index.html")