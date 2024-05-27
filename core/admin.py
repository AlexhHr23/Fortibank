import random
import uuid
from django.contrib import admin
from core.models import Ticket, Transaction, CreditCard, Evidence
from django.utils.html import format_html
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import io
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist


class TransactionAdmin(admin.ModelAdmin):
    list_editable  = ['amount', 'status','transaction_type','reciever', 'sender']
    list_display  = ['user', 'amount', 'status','transaction_type','reciever', 'sender']
    
class CredritCardAdmin(admin.ModelAdmin):
    list_editable  = ['amount', 'card_type', ]
    list_display  = ['user', 'amount', 'card_type']
  
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'open_image_preview', 'reviewed', 'validated', 'upload_date')
    list_filter = ('reviewed', 'validated')
    actions = ['validate_evidence', 'imprimir_boletos_validados']

    def open_image_preview(self, obj):
        if obj.photo:
            return format_html('<a href="#" class="open-image-preview" data-image-url="{}"><i class="fas fa-eye"></i></a>'.format(obj.photo.url))
        return "-"
    open_image_preview.short_description = 'Photo Preview'

    def validate_evidence(self, request, queryset):
        tickets = []
        for evidence in queryset:
            if not evidence.validated:
                evidence.reviewed = True
                evidence.validated = True
                evidence.save()
                # Verificar si ya existe un ticket para esta evidencia
                try:
                    ticket = Ticket.objects.get(evidence=evidence)
                except ObjectDoesNotExist:
                    ticket_number = self.generate_ticket_number()
                    ticket = Ticket.objects.create(
                        user=evidence.user,
                        evidence=evidence,
                        ticket_number=ticket_number
                    )
                tickets.append(ticket)

        if tickets:
            pdf = self.generar_boletos_pdf(tickets)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="boletos_validados.pdf"'
                self.message_user(request, "Las evidencias seleccionadas han sido validadas y se han emitido boletos.")
                return response
        else:
            self.message_user(request, "No se han emitido boletos ya que las evidencias seleccionadas ya estaban validadas.")
    
    validate_evidence.short_description = "Validar evidencia seleccionada"

    def imprimir_boletos_validados(self, request, queryset):
        evidencias_no_validadas = queryset.filter(validated=False)
        if evidencias_no_validadas.exists():
            self.message_user(request, "No se pueden imprimir boletos porque algunas evidencias no están validadas.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        usuarios = queryset.filter(validated=True).values_list('user', flat=True)
        boletos = Ticket.objects.filter(user__in=usuarios, evidence__validated=True)

        if boletos.exists():
            pdf = self.generar_boletos_pdf(boletos)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="boletos_validados.pdf"'
                return response
        else:
            self.message_user(request, "No hay boletos para los usuarios seleccionados.")
    
    imprimir_boletos_validados.short_description = "Imprimir Boletos Validados"

    def generate_ticket_number(self):
        return str(random.randint(1000, 9999))

    def generar_boletos_pdf(self, boletos):
        if not boletos:
            return None

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        boleto_width = 3.5 * inch
        boleto_height = 2 * inch
        margin = 0.5 * inch

        x = margin
        y = height - boleto_height - margin

        for boleto in boletos:
            if y < margin:
                c.showPage()
                y = height - boleto_height - margin

            c.setLineWidth(1)
            c.rect(x, y, boleto_width, boleto_height)

            c.setFont("Helvetica", 10)
            c.drawString(x + 0.1 * inch, y + boleto_height - 0.3 * inch, f"Nombre del usuario: {boleto.user.username}")
            c.drawString(x + 0.1 * inch, y + boleto_height - 0.6 * inch, f"Número del boleto: {boleto.ticket_number}")
            c.drawImage(boleto.evidence.photo.path, x + 0.1 * inch, y + 0.1 * inch, width=3.3 * inch, height=1.2 * inch)

            y -= boleto_height + margin

        c.save()
        buffer.seek(0)

        return buffer.getvalue()
        
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(CreditCard, CredritCardAdmin)
admin.site.register(Evidence, EvidenceAdmin)