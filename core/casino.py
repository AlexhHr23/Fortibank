from django.shortcuts import render
from .models import Account
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



@login_required
def casino_view(request):
    # Obtener los 5 usuarios con el mayor saldo
    top_users = Account.objects.order_by('-account_balance')[:5]
    # Pasar los datos a la plantilla
    return render(request, 'casino/casino.html', {'top_users': top_users})

