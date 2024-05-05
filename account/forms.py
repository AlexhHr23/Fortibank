from django import forms
from account.models import KYC
from django.forms import ImageField, FileInput, DateInput

class DateInput(forms.DateInput):
    input_type = 'date'
    
class KYCForm(forms.ModelForm):
    #identity_image = ImageField(widget=FileInput)
    image = ImageField(widget=FileInput)
    
    class Meta: 
        model = KYC
        fields = ['full_name','image','gender','date_of_birth','signature','mobile']
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full Name"}),
            "mobile": forms.TextInput(attrs={"placeholder": "Mobile"}), 
        }