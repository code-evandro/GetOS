from django import forms
from .models import Patrimonio


class PatrimonioForm(forms.ModelForm):
    class Meta:
        model = Patrimonio
        fields = ['descricao', 'setor', 'responsavel', 'status', 'observacao']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-input'}),
            'setor': forms.Select(attrs={'class': 'form-input'}),
            'responsavel': forms.Select(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'observacao': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth.models import User
        from setores.models import Setor
        self.fields['responsavel'].queryset = User.objects.filter(
            is_active=True
        ).order_by('username')
        self.fields['setor'].queryset = Setor.objects.all().order_by('nome')


class TransferenciaSetorForm(forms.Form):
    setor = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-input'}),
        label='Novo Setor'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from setores.models import Setor
        self.fields['setor'].queryset = Setor.objects.all().order_by('nome')


class TransferenciaResponsavelForm(forms.Form):
    responsavel = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-input'}),
        label='Novo Responsável'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth.models import User
        self.fields['responsavel'].queryset = User.objects.filter(
            is_active=True
        ).order_by('username')


class BaixaPatrimonioForm(forms.Form):
    motivo = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-input',
            'placeholder': 'Informe o motivo da baixa (obrigatório)...'
        }),
        label='Motivo da Baixa'
    )


class PatrimonioFilterForm(forms.Form):
    setor = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='Todos os Setores',
        widget=forms.Select(attrs={'class': 'form-input'}),
    )
    status = forms.ChoiceField(
        choices=[('', 'Todos os Status')] + list(Patrimonio.Status.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'}),
    )
    busca = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Buscar por número ou descrição...'
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from setores.models import Setor
        self.fields['setor'].queryset = Setor.objects.all().order_by('nome')
