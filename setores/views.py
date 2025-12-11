from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Setor
from .forms import SetorForm


def teste_layout(request):
    """
    View apenas para testar o novo layout com sidebar (getos/base.html).
    Não interfere nas telas reais do sistema.
    """
    return render(request, 'getos/teste_layout.html')


def cadastrar_setor(request):
    form = SetorForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Setor cadastrado com sucesso!')
            return redirect('cad_setor')
        else:
            messages.error(request, '❌ Preencha todos os campos corretamente.')

    return render(request, 'getos/cad_setor.html', {'form': form})


def listar_setores(request):
    setores = Setor.objects.all().order_by('nome')
    return render(request, 'getos/listar_setores.html', {'setores': setores})


def editar_setor(request, id):
    setor = get_object_or_404(Setor, id=id)
    form = SetorForm(request.POST or None, instance=setor)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Setor atualizado com sucesso!')
            return redirect('listar_setores')
        else:
            messages.error(request, '❌ Corrija os erros no formulário.')

    return render(request, 'getos/editar_setor.html', {'form': form})
