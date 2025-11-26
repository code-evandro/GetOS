from django.contrib import admin
from .models import Setor, Servidor, Tecnico, OrdemDeServico

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']

@admin.register(Servidor)
class ServidorAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'setor']
    search_fields = ['nome']
    list_filter = ['setor']

@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    search_fields = ['user__username']

@admin.register(OrdemDeServico)
class OrdemDeServicoAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'servidor', 'setor', 'tipo', 'tecnico', 'data',
        'finalizada', 'criado_em', 'atualizado_em'
    ]
    list_editable = ['finalizada']
    list_filter = ['setor', 'tipo', 'finalizada', 'data']
    search_fields = ['servidor__nome', 'tipo', 'tecnico__user__username']
    date_hierarchy = 'data'
    ordering = ['-data']
