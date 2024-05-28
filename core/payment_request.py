from django.shortcuts import redirect, render
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal

from core.models import Transaction

@login_required
def SearchUserRequest(request):
    account = Account.objects.all()
    query = request.POST.get("account_number")
    
    if query:
        account = account.filter(
            Q(account_number=query) |
            Q(account_id=query)
        ).distinct()
        
    context = {
        "account": account,
        "query": query
    }
    return render(request, "payment_request/search-users.html", context)


def AmountRequest(request, account_number):
    account = Account.objects.get(account_number=account_number)
    context = {
        "account": account
    }
    return render(request, "payment_request/amount-request.html", context)

def AmountRequestProcess(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except Account.DoesNotExist:
        messages.warning(request, "La cuenta no existe")
        return redirect("core:search-account")

    sender = request.user
    reciever = account.user

    sender_account = request.user.account
    reciever_account = account

    # Verificar si el usuario está intentando hacer una solicitud de pago a su propia cuenta
    if sender == reciever:
        messages.warning(request, "No puedes solicitar un pago a tu propia cuenta")
        return redirect("core:amount-request", account.account_number)

    if request.method == "POST":
        amount = request.POST.get("amount-request")
        description = request.POST.get("description")

        new_request = Transaction.objects.create(
            user=request.user,
            amount=amount,
            description=description,

            sender=sender,
            reciever=reciever,

            sender_account=sender_account,
            reciever_account=reciever_account,

            status="request_processing",
            transaction_type="request"
        )
        new_request.save()
        transaction_id = new_request.transaction_id
        return redirect("core:amount-request-confirmation", account.account_number, transaction_id)
    else:
        messages.warning(request, "Ocurrio un error. Intentelo más tarde.")
        return redirect("account:dashboard")

def AmountRequestConfirmation(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        "account": account,
        "transaction": transaction,
    }
    return render(request, "payment_request/amount-request-confirmation.html", context)


def AmountRequestFinalProcess(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == request.user.account.pin_number:
            transaction.status = "request_send"
            transaction.save()
            
            messages.success(request, "Su solicitud de pago ha sido enviada exitosamente")
            return redirect("core:amount-request-completed", account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, "Ocurrio un error. Intentalo más tarde")
        return redirect("account:dashboard")

def RequestCompleted(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
        "account": account,
        "transaction": transaction,
    }
    return render(request, "payment_request/amount-request-completed.html", context)


######### SETTLED
def settlement_confirmation(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
        "account": account,
        "transaction": transaction,
    }
    return render(request, "payment_request/settlement-confirmation.html", context)

def settlement_processing(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    sender = request.user
    sender_account = request.user.account
    
    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == request.user.account.pin_number:
            if sender_account.account_balance <= 0 or sender_account.account_balance < transaction.amount:
                messages.warning(request, "Fondos insuficientes, Encuentra tu cuenta y vuelve a intentarlo")
                return redirect('account:dashboard')
            else:
                sender_account.account_balance -= transaction.amount
                sender_account.save()
                
                account.account_balance += transaction.amount
                account.save()
                
                transaction.status = "request_settled"
                transaction.save()
                
                messages.success(request, f"La liquidación para {account.user.kyc.full_name} se realizó correctamente")
                return redirect("core:settlement-completed", account.account_number, transaction.transaction_id)
        else: 
            messages.warning(request, "Pin incorrecto")
            return redirect('core:settlement-confirmation', account.account_number, transaction.transaction_id)
    else: 
        messages.warning(request, "Ocurrio un error")
        return redirect('account:dashboard', account.account_number, transaction.transaction_id)

def settlement_completed(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
        "account": account,
        "transaction": transaction,
    }
    return render(request, "payment_request/settlement-completed.html", context)


def deletePaymentRequest(request, account_number, transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    if request.user == transaction.user:
        transaction.delete()
        messages.success(request, "Solicitud de pago eliminada correctamente")
        return redirect("core:transactions")
