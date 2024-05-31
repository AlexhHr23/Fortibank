from django.shortcuts import redirect, render
from django.http import HttpResponse

# def index(request):
#     if request.user.is_authenticated:
#         return redirect("account:dashboard")
#     return render(request, "userauths/sign-in.html")

def contact(request):
    return render(request, "core/contact.html")

def about(request):
    return render(request, "core/about.html")

