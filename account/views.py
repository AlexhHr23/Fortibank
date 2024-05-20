from django.shortcuts import render, redirect
from account.models import KYC, Account
from account.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CrediCardForm
from core.models import CreditCard





#@login_required
def account(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
              messages.warning(request, "Necesitas enviar tu formulario")
              return redirect("account:kyc-reg")   

        account = Account.objects.get(user=request.user)
    else:
        messages.warning(request, "Necesitas iniciar sesión para acceder")
        return redirect("userauths:sign-in")   

    context = {
        "kyc": kyc,
        "account": account,
    }
    return render(request, "account/account.html", context)

@login_required
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=user)

    try:
        kyc = KYC.objects.get(user=user)
    except:
        kyc = None

    if request.method == "POST":
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request, "formulario KYC enviado correctamente.")
            return redirect("core:index")
    else:
        form = KYCForm(instance=kyc) 
    context = {
        "account": account,
        "form": form,
        "kyc": kyc,
    }
    return render(request, "account/kyc-form.html", context)

def dashboard(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
              messages.warning(request, "Necesitas enviar tu formulario")
              return redirect("account:kyc-reg")   

        account = Account.objects.get(user=request.user)
        credit_card = CreditCard.objects.filter(user=request.user).order_by("-id")
        
        if request.method == "POST":
            form = CrediCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()
                
                card_id = new_form.card_id
                messages.success(request, "Card Added Successfuly")
                return redirect("account:dashboard")
        else:
            form = CrediCardForm()
    else:
        messages.warning(request, "Necesitas iniciar sesión para acceder")
        return redirect("userauths:sign-in")   

    context = {
        "kyc": kyc,
        "account": account,
        "form": form,
        "credit_card": credit_card,
    }
    return render(request, "account/dashboard.html", context)
