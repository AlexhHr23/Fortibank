from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout

from userauths.models import User
from django.contrib import messages


def RegisterView(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            #form.save()
            new_user = form.save() #new_user.email
            username = form.cleaned_data.get("username")
            #username = request.POST.get("username")
            messages.success(request, f"Hey {username} la cuenta fue creada correctamente.")
            #new_user = authenticate(username=form.cleand_data.get('email'))
            new_user = authenticate(username=form.cleaned_data['email'], 
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("account:account")
        
    if request.user.is_authenticated:
        messages.warning(request, f"Hey correcto.")
        return redirect("account:account")
    
    else:
        form = UserRegisterForm()
    context = {
        "form": form
    }
    return render(request, "userauths/sign-up.html", context)


def LoginView(request): 
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Inicio de sesión exitoso.")
                return redirect("account:account")
            else:
                messages.warning(request, "usuario o contraseña no es correcto")
                return redirect("userauths:sign-in")
        except: 
            messages.warning(request, "No existe el usuario")
        
    if request.user.is_authenticated:
        messages.warning(request, "Has iniciado sesión.")
        return redirect("account:account")
    
    return render(request, "userauths/sign-in.html")

def LogoutView(request):
    logout(request)
    messages.success(request, "Cierre de sesión")
    return redirect("userauths:sign-in")