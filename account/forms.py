from django import forms
from account.models import KYC
from django.forms import ImageField, FileInput, DateInput

class DateInput(forms.DateInput):
    input_type = 'date'
    
class KYCForm(forms.ModelForm):
    #identity_image = ImageField(widget=FileInput)
    image = ImageField(widget=FileInput)
    #signature = ImageField(widget=FileInput)
    
    class Meta: 
        model = KYC
        fields = ['image', 'marrital_status', 'gender', 'date_of_birth','state', 'city','company']
        widgets = {
            #"fax": forms.TextInput(attrs={"placeholder": "Número de fax"}), 
            "state": forms.TextInput(attrs={"placeholder": "Estado"}), 
            "city": forms.TextInput(attrs={"placeholder": "Ciudad"}), 
            'date_of_birth':DateInput
        }