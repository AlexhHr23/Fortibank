from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import CreditCard
from account.models import Account

def card_detail(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    context = {
        "account": account,
        "credit_card": credit_card,
    }
    
    return render(request, "credit_card/card-detail.html", context)

def withdraw_fund(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    
    amount_str = request.POST.get("amount")
    try:
        # Elimina cualquier carácter no numérico (como comas o puntos) del valor
        amount_cleaned = amount_str.replace(",", "").replace(".", "")
        amount_decimal = Decimal(amount_cleaned)
    except:
        messages.warning(request, "Cantidad no válida")
        return redirect("core:card-detail", credit_card.card_id)
    
    if credit_card.amount >= amount_decimal and credit_card.amount != 0.00:
        account.account_balance += amount_decimal
        account.save()
        messages.success(request, "Retiro exitoso")
    else:
        messages.warning(request, "Fondos insuficientes")
    
    return redirect("core:card-detail", credit_card.card_id)


def delete_card(request, card_id):
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    
    account = request.user.account
    
    if credit_card.amount > 0:
        account.account_balance += credit_card.amount
        account.save()
        
        credit_card.delete()
        messages.success(request, "Tarjeta elimininada exitosamente")
        return redirect("account:dashboard")
    
    credit_card.delete()
    messages.success(request,"Tarjeta elimininada exitosamente")
    return redirect("account:dashboard")


def found_credit_card(request, card_id):
    
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    account = request.user.account
    
    if request.method == "POST":
        amount = request.POST.get("funding_amount")
        
        if Decimal(amount) <= account.account_balance:
            account.account_balance -= Decimal(amount)
            account.save()
            
            credit_card.amount += Decimal(amount)
            credit_card.save()
            
            messages.success(request, "Financiamiento exitoso")
            return redirect("core:card-detail", credit_card.card_id)
        else:
            messages.warning(request, "Fondos insuficientes")
            return redirect("core:card-detail", credit_card.card_id)