from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta, date
import json

from ordens.models import OrdemDeServico
from setores.models import Setor
from servidores.models import Servidor

@login_required
def menu(request):
    return render(request, 'getos/menu.html')

@login_required
def dashboard(request):
    hoje = date.today()
    ultimos_7_dias = hoje - timedelta(days=7)

    total_os = OrdemDeServico.objects.count()
    os_abertas = OrdemDeServico.objects.filter(finalizada=False).count()
    os_finalizadas = OrdemDeServico.objects.filter(finalizada=True).count()

    os_ultimos_dias = OrdemDeServico.objects.filter(data__gte=ultimos_7_dias).order_by('-data')

    os_por_setor = OrdemDeServico.objects.values('setor__nome').annotate(qtd=Count('id')).order_by('-qtd')[:5]
    os_por_tecnico = OrdemDeServico.objects.values('tecnico__user__username').annotate(qtd=Count('id')).order_by('-qtd')[:5]

    # Gráfico de OS por mês (últimos 12 meses)
    os_por_mes = OrdemDeServico.objects.annotate(
        mes=TruncMonth('data')
    ).values('mes').annotate(qtd=Count('id')).order_by('mes')

    labels = [item['mes'].strftime('%b/%y') for item in os_por_mes]
    dados = [item['qtd'] for item in os_por_mes]

    dados_grafico = json.dumps({
        'labels': labels,
        'dados': dados
    })

    context = {
        'total_os': total_os,
        'os_abertas': os_abertas,
        'os_finalizadas': os_finalizadas,
        'os_por_setor': list(os_por_setor),
        'os_por_tecnico': list(os_por_tecnico),
        'os_ultimos_dias': os_ultimos_dias,
        'dados_grafico': dados_grafico,
    }

    return render(request, 'getos/dashboard.html', context)

# 🔓 View para logout com redirecionamento
def logout_redirect(request):
    logout(request)
    return redirect('login')
