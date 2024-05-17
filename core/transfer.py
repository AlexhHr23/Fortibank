from django.shortcuts import redirect, render
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal

from core.models import Transaction


@login_required
def search_users_account_number(request):
    # account = Account.objects.filter(account_status="active")
    account = Account.objects.all()
    query = request.POST.get("account_number")

    if query:
        account = account.filter(
            Q(account_number=query) | Q(account_id=query)
        ).distinct()

    context = {
        "account": account,
        "query": query,
    }
    return render(request, "transfer/search-user-by-account-number.html", context)


def AmountTransfer(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except:
        messages.warning(request, "La cuenta no existe")
        return redirect("core:search-account")
    context = {
        "account": account,
    }
    return render(request, "transfer/amount-transfer.html", context)


def AmountTransferProcess(request, account_number):
    account = Account.objects.get(
        account_number=account_number
    )  # Get the account that the money vould be sent to
    sender = request.user  # get the person that is logget in
    reciever = (
        account.user
    )  # The account of the person that is going to reciver the money

    sender_account = request.user.account
    reciever_account = account

    if request.method == "POST":
        amount = request.POST.get("amount-send")
        description = request.POST.get("description")

        if sender_account.account_balance >= Decimal(amount):
            new_transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                description=description,
                reciever=reciever,
                sender=sender,
                sender_account=sender_account,
                reciever_account=reciever_account,
                status="processing",
                transaction_type="transfer",
            )
            new_transaction.save()

            # Obtener la identificación de la transacción que se creó
            transaction_id = new_transaction.transaction_id
            return redirect(
                "core:transfer-confirmation", account.account_number, transaction_id
            )
        else:
            messages.warning(request, "Fondos insuficientes")
            return redirect("core:amount-transfer", account.account_number)
    else:
        messages.warning(
            request, "Se ha producido un error. Vuelve a intentarlo más tarde."
        )
        return redirect("account:account")


def TransferConfirmation(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)

    except:
        messages.warning(request, "La transacción no existe.")
        return redirect("account:account")
    context = {
        "account": account, 
        "transaction": transaction
    }
    return render(request, "transfer/transfer-confirmation.html", context)

def TransferProcess(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    sender = request.user  
    reciever = (account.user) 

    sender_account = request.user.account
    reciever_account = account
    
    completed = False
    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        
        if pin_number == sender_account.pin_number:
            transaction.status = "completed"
            transaction.save()
            
            # Descuenta el monto que envia el usuario desde su cuenta
            sender_account.account_balance -= transaction.amount
            sender_account.save()
            
            #Agrega el monto que se eliminó de la cuenta a la persona a la que también se le envío el dinero.
            account.account_balance += transaction.amount
            account.save()
            
            messages.success(request, "Trasnferencia exitosa")
            return redirect("core:transfer-completed",  account.account_number,  transaction.transaction_id)
        else:
            messages.warning(request, "Pin Incorrecto.")
            return redirect('core:settled_confirmation', account.account_number,  transaction.transaction_id)
    else:
        messages.warning(request, "Ocurrio un error, Intentalo más tarde.")
        return redirect('account:account')
    
def TransferCompleted(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)

    except:
        messages.warning(request, "La transferencia no existe.")
        return redirect("account:account")
    context = {
        "account": account, 
        "transaction": transaction
    }
    return render(request, "transfer/transfer-completed.html", context)
    


    
