from django.contrib import admin
from core.models import Transaction, CreditCard

class TransactionAdmin(admin.ModelAdmin):
    list_editable  = ['amount', 'status','transaction_type','reciever', 'sender']
    list_display  = ['user', 'amount', 'status','transaction_type','reciever', 'sender']
    
class CredritCardAdmin(admin.ModelAdmin):
    list_editable  = ['amount', 'card_type', ]
    list_display  = ['user', 'amount', 'card_type']

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(CreditCard, CredritCardAdmin)
