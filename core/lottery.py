import io
import textwrap
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from account.models import KYC
from .forms import EvidenceForm
from .models import Evidence, Account, Ticket

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from account.models import KYC
from .forms import EvidenceForm
from .models import Evidence, Account

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from django.utils.html import format_html


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
        return redirect('core:evidence-completed')

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

@login_required
def evidence_completed(request):
    return render(request, 'lottery/evidence-completed.html')

@login_required
def download_ticket(request):
    user = request.user
    ticket = get_object_or_404(Ticket, user=user, evidence__validated=True)

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    boleto_width = 2 * inch
    boleto_height = 3.9 * inch  
    margin = 0.5 * inch

    x = margin
    y = height - boleto_height - margin

    c.setLineWidth(1)
    c.rect(x, y, boleto_width, boleto_height)

    c.setFont("Helvetica", 10)

    image_width = 1.8 * inch
    image_height = 2.8 * inch
    image_x = x + 0.1 * inch  
    image_y = y + boleto_height - 3 * inch  
    c.drawImage(ticket.evidence.photo.path, image_x, image_y, width=image_width, height=image_height)

    text_x = x + 0.1 * inch 
    text_y = y + 0.65 * inch  

    # Obtener el nombre completo y el nombre de la empresa del modelo KYC
    try:
        kyc_info = user.kyc  # Asumiendo que existe una relación OneToOne entre User y KYC
        full_name = kyc_info.full_name
        company_name = kyc_info.company
    except KYC.DoesNotExist:
        full_name = "Nombre no disponible"
        company_name = "Empresa no disponible"

    # Dividir el nombre completo y el nombre de la empresa en líneas si es necesario
    max_text_width = boleto_width - 0.2 * inch  
    lines_full_name = textwrap.wrap(full_name, width=30) 
    lines_company_name = textwrap.wrap(f"Empresa: {company_name}", width=30)

    # Imprimir el nombre completo
    for line in lines_full_name:
        if text_y < y + 0.1 * inch:  
            break
        c.drawString(text_x, text_y, line)
        text_y -= 0.15 * inch  

    # Asegurar que haya espacio entre el nombre completo y la empresa
    if text_y < y + 0.1 * inch:
        text_y = y + 0.1 * inch

    # Imprimir el nombre de la empresa
    for line in lines_company_name:
        if text_y < y + 0.1 * inch:  
            break
        c.drawString(text_x, text_y, line)
        text_y -= 0.15 * inch  

    # Asegurar que el número del boleto esté siempre visible
    if text_y < y + 0.1 * inch:
        text_y = y + 0.1 * inch

    c.drawString(text_x, text_y - 0.25 * inch, f"Número del boleto: {ticket.ticket_number}")

    y -= boleto_height + margin

    c.save()
    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="boleto_{ticket.ticket_number}.pdf"'
    return response

@login_required
def evidence_completed(request):
    try:
        ticket = Ticket.objects.get(user=request.user, evidence__validated=True)
    except Ticket.DoesNotExist:
        ticket = None

    return render(request, 'lottery/evidence-completed.html', {'ticket': ticket})