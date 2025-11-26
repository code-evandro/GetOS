from django import forms
from .models import Servidor

class ServidorForm(forms.ModelForm):
    class Meta:
        model = Servidor
        fields = ['nome', 'matricula', 'setor']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'matricula': forms.NumberInput(attrs={'class': 'form-input'}),
            'setor': forms.Select(attrs={'class': 'form-select'}),
        }
