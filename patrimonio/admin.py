from django.contrib import admin
from .models import Patrimonio, HistoricoPatrimonio


class HistoricoPatrimonioInline(admin.TabularInline):
    model = HistoricoPatrimonio
    extra = 0
    readonly_fields = [
        'tipo_movimento', 'descricao', 'setor_anterior', 'setor_novo',
        'responsavel_anterior', 'responsavel_novo', 'status_anterior',
        'status_novo', 'motivo_baixa', 'usuario', 'data',
    ]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Patrimonio)
class PatrimonioAdmin(admin.ModelAdmin):
    list_display = [
        'numero', 'descricao', 'setor', 'responsavel',
        'status', 'criado_em', 'atualizado_em',
    ]
    list_filter = ['setor', 'status']
    search_fields = ['numero', 'descricao']
    list_editable = ['status']
    readonly_fields = ['numero', 'criado_em', 'atualizado_em']
    inlines = [HistoricoPatrimonioInline]


@admin.register(HistoricoPatrimonio)
class HistoricoPatrimonioAdmin(admin.ModelAdmin):
    list_display = [
        'patrimonio', 'tipo_movimento', 'usuario', 'data'
    ]
    list_filter = ['tipo_movimento', 'data']
    search_fields = ['patrimonio__numero', 'descricao']
    readonly_fields = [
        'patrimonio', 'tipo_movimento', 'descricao', 'setor_anterior',
        'setor_novo', 'responsavel_anterior', 'responsavel_novo',
        'status_anterior', 'status_novo', 'motivo_baixa', 'usuario', 'data',
    ]
    ordering = ['-data']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
