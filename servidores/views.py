from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Servidor
from .forms import ServidorForm

def cadastrar_servidor(request):
    form = ServidorForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Servidor cadastrado com sucesso!')
            return redirect('cad_servidor')
        else:
            messages.error(request, '❌ Preencha todos os campos corretamente.')

    return render(request, 'getos/cad_servidor.html', {'form': form})


def listar_servidores(request):
    servidores = Servidor.objects.select_related('setor').order_by('nome')
    return render(request, 'getos/listar_servidores.html', {'servidores': servidores})


def editar_servidor(request, id):
    servidor = get_object_or_404(Servidor, id=id)
    form = ServidorForm(request.POST or None, instance=servidor)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Servidor atualizado com sucesso!')
            return redirect('listar_servidores')
        else:
            messages.error(request, '❌ Corrija os erros no formulário.')

    return render(request, 'getos/editar_servidor.html', {'form': form})
