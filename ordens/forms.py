from django import forms
from .models import OrdemDeServico, Tecnico, Servidor

class OrdemDeServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemDeServico
        fields = ['servidor', 'tipo', 'tecnico', 'data', 'relato']  # Removido 'setor' e 'ramal'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'relato': forms.Textarea(attrs={'rows': 4, 'class': 'form-input'}),
            'tipo': forms.TextInput(attrs={'class': 'form-input'}),
            'servidor': forms.Select(attrs={'class': 'form-input', 'id': 'id_servidor'}),
            'tecnico': forms.Select(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tecnico'].queryset = Tecnico.objects.select_related('user').order_by('user__username')
        self.fields['servidor'].queryset = Servidor.objects.all().order_by('nome')

# Novo formulário para finalização da OS
class FinalizarOSForm(forms.ModelForm):
    class Meta:
        model = OrdemDeServico
        fields = ['comentario_tecnico']
        widgets = {
            'comentario_tecnico': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva o que foi feito...',
                'class': 'form-input',
            }),
        }
