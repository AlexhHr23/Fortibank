from django.db import models
import uuid
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
from django.db.models.signals import post_save

ACCOUNT_STATUS = (
    ("active", "Activo"),
    ("pending", "Pendiente"),
    ("in-active", "Inactivo")
)

MARITAL_STATUS = (
    ("married", "Casado"),
    ("single", "Soltero")
)

GENDER = (
    ("male", "Hombre"),
    ("female", "Mujer"),
    ("other", "Otro")
)

COMPANY = (
    ("AB FORTI", "AB FORTI"),
    ("INNOVET", "INNOVET"),
    ("UPPER LOGISTICS", "UPPER LOGISTICS"),
    ("BE EXEN", "BE EXEN")
)


# IDENTITY_TYPE = (
#     ("national_id_card", "INE"),
#     ("drivers_licence", "Licencia de conducir"),
#     ("international_passport", "Pasaporte")
# )


def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s_%s" % (instance,id, ext)
    return "user_{0}/{1}".format(instance.user.id, filename)

class Account(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default = uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) # 123 345 56 567
    account_number = ShortUUIDField(unique=True, length=10, max_length=25, prefix="217", alphabet="1234567890") #12345567678789
    account_id = ShortUUIDField(unique=True, length=7, max_length=25, prefix="DEX", alphabet="1234567890") #12345567678789
    pin_number = ShortUUIDField(unique=True, length=4, max_length=7, alphabet="1234567890") # 2743
    red_code = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh1234567890") # 2743unique=TRUE,
    account_status = models.CharField(max_length=100, choices=ACCOUNT_STATUS, default="active")
    date = models.DateTimeField(auto_now_add=True)
    kyc_submitted = models.BooleanField(default=False)
    kyc_confirmed = models.BooleanField(default=False)
    recommended_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="recommended")
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.user}"
    
class KYC(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True)
    #full_name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="kyc", default="default.jpg")
    #nationality = models.CharField(max_length=100)
    marrital_status = models.CharField(choices=MARITAL_STATUS, max_length=40)
    gender = models.CharField(choices=GENDER, max_length=40)
    #identity_type = models.CharField(choices=IDENTITY_TYPE, max_length=140)
    #identity_image = models.ImageField(upload_to="kyc", null=True, blank=True)
    date_of_birth = models.DateTimeField(auto_now_add=False)
    #signature = models.ImageField(upload_to="kyc")
    company = models.CharField(choices=COMPANY, max_length=50, default="AB FORTI")
    
    #address
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    
    #Contact Detail
    #mobile = models.CharField(max_length=1000)
    #fax = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.user}"


    
    
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

def save_account(sender, instance, **kwargs):
    instance.account.save()
    
post_save.connect(create_account, sender=User)
post_save.connect(save_account, sender=User)
