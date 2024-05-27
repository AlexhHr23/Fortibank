from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from account.models import KYC
from .forms import EvidenceForm
from .models import Evidence, Account

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from account.models import KYC
from .forms import EvidenceForm
from .models import Evidence, Account

@login_required
def upload_evidence(request):
    account = Account.objects.get(user=request.user)
    kyc = KYC.objects.get(user=request.user)
    
    try:
        evidence = Evidence.objects.get(user=request.user)
    except Evidence.DoesNotExist:
        evidence = None
    
    if evidence and evidence.validated:
        messages.error(request, 'Tu evidencia ya ha sido validada y no puedes subir otra.')
        return redirect('confirmacion_evidencia')

    if request.method == 'POST':
        form = EvidenceForm(request.POST, request.FILES, instance=evidence)
        if form.is_valid():
            evidence = form.save(commit=False)
            evidence.user = request.user
            evidence.reviewed = False
            evidence.validated = False
            evidence.save()
            
            messages.success(request, "Evindecia enviada correctamente.")
            return redirect('account:dashboard')
        
    else:
        form = EvidenceForm(instance=evidence)
        
    context = {
        "form": form,
        "account": account,
        "kyc": kyc
    }
    
    return render(request, 'lottery/upload_evidence.html', context)
    