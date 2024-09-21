from django import forms
from .models import Order
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class OrderForm(forms.ModelForm):
    user_name = forms.CharField(label="Nom d'utilisateur" ,max_length=100, disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    user_email = forms.EmailField(label="adresse mail" ,disabled=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    user_phone = forms.CharField(label="Numéro téléphone" ,max_length=15,validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                    message="Entrez un bon numéro de téléphone",
                    code='invalid_phone_number'
            )],required=False ,widget=forms.TextInput(attrs={'class': 'form-control'}))
    delivery_address = forms.CharField(label="adresse de livraison", max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    


    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('user_phone')
        
        if phone_number:
            # Si un numéro est fourni, applique les validations
            # Assure-toi que la validation regex est respectée
            return phone_number
        else:
            # Si le champ est vide, retourne None (ou ne fais rien)
            return None

    class Meta:
        model = Order
        fields = ['user_name', 'user_email', 'user_phone', 'delivery_address']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['user_name'].initial = user.username
            self.fields['user_email'].initial = user.email
            self.fields['user_phone'].initial = getattr(user, 'profile.phone', '')  # Supposons que le numéro de téléphone est dans le profil de l'utilisateur
