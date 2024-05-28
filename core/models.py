import uuid
from django.db import models
from userauths.models import User
from account.models import Account
from shortuuid.django_fields import ShortUUIDField

TRANSACTION_TYPE = (
    ("trasnfer", "Transferir"),
    ("recieved", "Recivir"),
    ("withdraw", "Retirar"),
    ("refund", "Reembolso"),
    ("request", "Payment Request"),
    ("none", "Ninguno"),
)


TRANSACTION_STATUS = (
    ("failed", "fallido"),
    ("completed", "completado"),
    ("pending", "pendiente"),
    ("processing", "procesando"),
    ("requested", "solicitado"),
    ("request_send", "solicitud enviada"),
    ("request_settled", "solicitud resuelta"),
    ("request_processing", "solicitud en proceso")
)

CARD_TYPE = (
    ("master", "master"),
    ("visa", "visa"),
    ("verve", "verve"),
)


class Transaction(models.Model):
    transaction_id = ShortUUIDField(unique=True, length=15, max_length=20, prefix="TRN")
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    description = models.CharField(max_length=1000, null=True, blank=True)
    
    reciever = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="receiver")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    
    reciever_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="reciever_account")
    sender_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="sender_account")
    
    status = models.CharField(choices=TRANSACTION_STATUS, max_length=100, default="pending")
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, max_length=100, default="none")
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    
    def __str__(self):
        try:
            return f"{self.user}"
        except:
            return f"Transaccion"
        

class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_id = ShortUUIDField(unique=True, length=5, max_length=20, prefix="CARD", alphabet="1234567890")
    
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    cvv = models.IntegerField()
    
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    card_type = models.CharField(choices=CARD_TYPE, max_length=20, default="master")
    card_status = models.BooleanField(default=True)
    
    daet = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}"
    
    

class Evidence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='evidences/')
    reviewed = models.BooleanField(default=False)
    validated = models.BooleanField(default=False)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.upload_date}"
    
class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default = uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    evidence = models.OneToOneField(Evidence, on_delete=models.CASCADE)
    ticket_number = ShortUUIDField(unique=True, length=4, max_length=4, prefix="217", alphabet="1234567890")
    date_issue = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}"
    
class EvidenceWithPersons(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='evidences_persons/')
    reviewed = models.BooleanField(default=False)
    validated = models.BooleanField(default=False)
    upload_date = models.DateTimeField(auto_now_add=True)
    deposit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    
    def __str__(self):
        return f"{self.user}"
     