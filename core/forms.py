from django import forms
from account.models import KYC
from core.models import CreditCard, Evidence, EvidenceWithPersons


class CrediCardForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Card Holder Name"}))
    number = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder": "Card number"}))
    month = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder": "Expiry Month"}))
    year = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder": "Expiry Month"}))
    cvv = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder": "CVV"}))
    
    
    class Meta:
        model = CreditCard
        fields = ['name','number','month', 'year', 'cvv', 'card_type']
        
class EvidenceForm(forms.ModelForm):
    class Meta:
        model = Evidence
        fields = ['photo']
        
class EvidenceWithPersonsForm(forms.ModelForm):
    class Meta:
        model = EvidenceWithPersons
        fields = ['photo']