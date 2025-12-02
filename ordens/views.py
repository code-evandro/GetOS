from django.conf import settings 
import os  

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.contrib import messages
from .models import OrdemDeServico
from .forms import OrdemDeServicoForm, FinalizarOSForm
from servidores.models import Servidor
from setores.models import Setor
from .models import Tecnico
from xhtml2pdf import pisa
import io

def visualizar_os(request):
    ordens = OrdemDeServico.objects.select_related('tecnico__user', 'servidor', 'setor')

    # Filtros via GET
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    tecnico_id = request.GET.get('tecnico')
    setor_id = request.GET.get('setor')
    servidor_id = request.GET.get('servidor')
    situacao = request.GET.get('situacao')

    if data_inicio:
        ordens = ordens.filter(data__gte=data_inicio)
    if data_fim:
        ordens = ordens.filter(data__lte=data_fim)
    if tecnico_id:
        ordens = ordens.filter(tecnico__id=tecnico_id)
    if setor_id:
        ordens = ordens.filter(setor__id=setor_id)
    if servidor_id:
        ordens = ordens.filter(servidor__id=servidor_id)
    if situacao == 'aberta':
        ordens = ordens.filter(finalizada=False)
    elif situacao == 'finalizada':
        ordens = ordens.filter(finalizada=True)

    
    tecnicos = Tecnico.objects.select_related('user').order_by('user__username')
    servidores = Servidor.objects.all().order_by('nome')
    setores = Setor.objects.all().order_by('nome')

    return render(request, 'getos/visualizar_os.html', {
        'ordens': ordens,
        'tecnicos': tecnicos,
        'servidores': servidores,
        'setores': setores
    })

def cadastrar_ordem(request):
    if request.method == 'POST':
        form = OrdemDeServicoForm(request.POST)
        if form.is_valid():
            ordem = form.save(commit=False)
            ordem.setor = ordem.servidor.setor
            ordem.ramal = ordem.servidor.setor.ramal
            ordem.save()
            messages.success(request, 'Ordem de Serviço cadastrada com sucesso!')
            return redirect('abrir_os')
        else:
            messages.error(request, 'Corrija os erros antes de salvar.')
    else:
        form = OrdemDeServicoForm()

    return render(request, 'getos/cad_ordem.html', {'form': form})

def finalizar_os(request, os_id):
    ordem = get_object_or_404(OrdemDeServico, id=os_id)
    if request.method == 'POST':
        form = FinalizarOSForm(request.POST, instance=ordem)
        if form.is_valid():
            ordem = form.save(commit=False)
            ordem.finalizada = True
            ordem.save()
            messages.success(request, 'OS finalizada com sucesso!')
            return redirect('visualizar_os')
        else:
            messages.error(request, 'Corrija os erros antes de finalizar.')
    else:
        form = FinalizarOSForm(instance=ordem)

    return render(request, 'getos/finalizar_os.html', {'form': form, 'ordem': ordem})

def gerar_pdf_os(request, id):
    ordem = get_object_or_404(OrdemDeServico, id=id)
    template = get_template('getos/pdf_ordem.html')

    
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'imgs', 'logo.png')

    html = template.render({
        'ordem': ordem,
        'logo_path': logo_path
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ordem_{id}.pdf"'

    pisa_status = pisa.CreatePDF(io.BytesIO(html.encode('utf-8')), dest=response)

    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    return response

def info_servidor(request, servidor_id):
    servidor = get_object_or_404(Servidor, id=servidor_id)
    setor = servidor.setor
    return JsonResponse({
        'setor': setor.nome,
        'ramal': setor.ramal
    })
