from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import timedelta, date
from ordens.models import OrdemDeServico
import json

def dashboard(request):
    hoje = date.today()
    sete_dias_atras = hoje - timedelta(days=7)

    total_os = OrdemDeServico.objects.count()
    os_abertas = OrdemDeServico.objects.filter(finalizada=False).count()
    os_finalizadas = OrdemDeServico.objects.filter(finalizada=True).count()
    os_ultimos_dias = OrdemDeServico.objects.filter(data__gte=sete_dias_atras).order_by('-data')

    os_por_setor = OrdemDeServico.objects.values('setor__nome').annotate(qtd=Count('id')).order_by('-qtd')[:5]
    os_por_tecnico = OrdemDeServico.objects.values('tecnico__user__username').annotate(qtd=Count('id')).order_by('-qtd')[:5]

    os_por_mes = OrdemDeServico.objects.annotate(
        mes=TruncMonth('data')
    ).values('mes').annotate(qtd=Count('id')).order_by('mes')

    labels = [item['mes'].strftime('%b/%y') for item in os_por_mes]
    dados = [item['qtd'] for item in os_por_mes]

    dados_grafico = json.dumps({
        'labels': labels,
        'dados': dados
    })

    return render(request, 'getos/dashboard.html', {
        'total_os': total_os,
        'os_abertas': os_abertas,
        'os_finalizadas': os_finalizadas,
        'os_ultimos_dias': os_ultimos_dias,
        'os_por_setor': os_por_setor,
        'os_por_tecnico': os_por_tecnico,
        'dados_grafico': dados_grafico,
    })
