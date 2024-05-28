from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import KYC
from .models import Evidence, Account, EvidenceWithPersons

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from account.models import KYC
from .forms import EvidenceWithPersonsForm

@login_required
def upload_evidence_persons(request):
    account = Account.objects.get(user=request.user)
    kyc = KYC.objects.get(user=request.user)
    
    try:
        evidence = EvidenceWithPersons.objects.get(user=request.user)
    except EvidenceWithPersons.DoesNotExist:
        evidence = None
    
    if evidence and evidence.validated:
        messages.error(request, 'Tu evidencia ya ha sido validada y no puedes subir otra.')
        return redirect('core:completed-evidence-persons')

    if request.method == 'POST':
        form = EvidenceWithPersonsForm(request.POST, request.FILES, instance=evidence)
        if form.is_valid():
            evidence = form.save(commit=False)
            evidence.user = request.user
            evidence.reviewed = False
            evidence.validated = False
            evidence.save()
            
            messages.success(request, "Evindecia enviada correctamente.")
            return redirect('account:dashboard')
        
    else:
        form = EvidenceWithPersonsForm(instance=evidence)
        
    context = {
        "form": form,
        "account": account,
        "kyc": kyc
    }
    
    return render(request, 'deposit/upload-evidence-persons.html', context)

@login_required
def completed_persons_evidence(request):
    return render(request, 'deposit/completed-evidence-persons.html')
    