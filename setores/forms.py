from django import forms
from .models import Setor

class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ['nome', 'sigla', 'secretaria', 'ramal']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'sigla': forms.TextInput(attrs={'class': 'form-input'}),
            'secretaria': forms.TextInput(attrs={'class': 'form-input'}),
            'ramal': forms.TextInput(attrs={'class': 'form-input'}),
        }
