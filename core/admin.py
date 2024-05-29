import random
import uuid
from django.contrib import admin
from core.models import EvidenceWithPersons, Ticket, Transaction, CreditCard, Evidence, Account
from django.utils.html import format_html
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import io
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal

class TransactionAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_editable  = ['amount', 'status','transaction_type','reciever', 'sender']
    list_display  = ['user', 'amount', 'status','transaction_type','reciever', 'sender']
    
class CredritCardAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_editable  = ['amount', 'card_type', ]
    list_display  = ['user', 'amount', 'card_type']
  
class EvidenceAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('user', 'view_evidence','reviewed', 'validated', 'upload_date', )
    list_filter = ('reviewed', 'validated')
    actions = ['validate_evidence', 'imprimir_boletos_validados']

    def view_evidence(self, obj):
        return format_html(
            '<a href="#" class="view-evidence" data-url="{}"><i class="fas fa-eye"></i></a>',
            obj.photo.url
        )
    view_evidence.short_description = "Ver Evidencia"


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
    

class Save(admin.SimpleListFilter):
    list_per_page = 25
    title = 'Saved'
    parameter_name = 'deposit_filter'

    def lookups(self, request, model_admin):
        return (
            ('gt_zero', 'Guardados'),
            ('le_zero', 'No guardados'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'gt_zero':
            return queryset.filter(deposit__gt=Decimal('0.00'))
        elif self.value() == 'le_zero':
            return queryset.filter(deposit__lte=Decimal('0.00'))
        return queryset
    

class EvidenceWithPersonsAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ['user', 'view_evidence', 'deposit', 'validated', 'upload_date']
    list_filter = ['validated', Save]  # Agregar el filtro personalizado
    list_editable = ['deposit']
    actions = ['Validar_Depositar']
    fields = ['user', 'photo', 'deposit', 'validated']

    def view_evidence(self, obj):
        return format_html(
            '<a href="#" class="view-evidence" data-url="{}"><i class="fas fa-eye"></i></a>',
            obj.photo.url
        )
    view_evidence.short_description = "Ver Evidencia"
    
    def Validar_Depositar(self, request, queryset):
        updated = 0
        for evidence in queryset:
            if not evidence.validated:
                deposit_amount = evidence.deposit
                evidence.validated = True
                evidence.save()

                # Agregar dinero a la cuenta del usuario asociado a la evidencia
                account = Account.objects.get(user=evidence.user)
                account.account_balance += deposit_amount
                account.save()
                updated += 1

        if updated > 0:
            self.message_user(request, f'{updated} evidencias validadas y saldo actualizado.')
        else:
            self.message_user(request, 'No se actualizaron evidencias ya que todas estaban validadas.')
            
            
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(CreditCard, CredritCardAdmin)
admin.site.register(Evidence, EvidenceAdmin)
admin.site.register(EvidenceWithPersons, EvidenceWithPersonsAdmin)