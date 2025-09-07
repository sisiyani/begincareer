from django import forms
from .models import Appointment
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact  # Lier le formulaire au modèle Contact
        fields = ['name', 'phone', 'email', 'budget', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Votre nom / prénom*', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Votre téléphone*', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Votre e-mail*', 'class': 'form-control'}),
            'budget': forms.TextInput(attrs={'placeholder': 'Mon budget estimé...', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message*', 'class': 'form-control', 'rows': 4}),
        }