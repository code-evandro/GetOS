from django.db import models
from django.contrib.auth.models import User
from setores.models import Setor


class Patrimonio(models.Model):
    class Status(models.TextChoices):
        ATIVO = 'ativo', 'Ativo'
        MANUTENCAO = 'manutencao', 'Manutenção'
        BAIXADO = 'baixado', 'Baixado'
        INATIVO = 'inativo', 'Inativo'

    numero = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name='Número do Patrimônio'
    )
    descricao = models.CharField(max_length=200)
    setor = models.ForeignKey(
        Setor,
        on_delete=models.PROTECT,
        related_name='patrimonios'
    )
    responsavel = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='patrimonios_responsavel'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ATIVO
    )
    observacao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['numero']
        verbose_name = 'Patrimônio'
        verbose_name_plural = 'Patrimônios'

    def __str__(self):
        return f"{self.numero} - {self.descricao}"

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = self._gerar_numero()
        super().save(*args, **kwargs)

    def _gerar_numero(self):
        from datetime import datetime
        ano = datetime.now().year
        ultimo = Patrimonio.objects.filter(
            numero__startswith=f'{ano}'
        ).order_by('numero').last()
        if ultimo:
            try:
                seq = int(ultimo.numero.split('-')[1]) + 1
            except (IndexError, ValueError):
                seq = 1
        else:
            seq = 1
        return f'{ano}-{seq:05d}'

    @property
    def status_badge_class(self):
        return {
            'ativo': 'bg-success',
            'manutencao': 'bg-warning text-dark',
            'baixado': 'bg-danger',
            'inativo': 'bg-secondary',
        }.get(self.status, 'bg-secondary')


class HistoricoPatrimonio(models.Model):
    class TipoMovimento(models.TextChoices):
        CRIACAO = 'criacao', 'Criação'
        TRANSFERENCIA_SETOR = 'transferencia_setor', 'Transferência de Setor'
        TRANSFERENCIA_RESPONSAVEL = 'transferencia_responsavel', 'Transferência de Responsável'
        ALTERACAO_STATUS = 'alteracao_status', 'Alteração de Status'
        BAIXA = 'baixa', 'Baixa'
        EDICAO = 'edicao', 'Edição'

    patrimonio = models.ForeignKey(
        Patrimonio,
        on_delete=models.PROTECT,
        related_name='historico'
    )
    tipo_movimento = models.CharField(
        max_length=30,
        choices=TipoMovimento.choices
    )
    descricao = models.TextField()
    setor_anterior = models.CharField(max_length=100, blank=True, null=True)
    setor_novo = models.CharField(max_length=100, blank=True, null=True)
    responsavel_anterior = models.CharField(max_length=100, blank=True, null=True)
    responsavel_novo = models.CharField(max_length=100, blank=True, null=True)
    status_anterior = models.CharField(max_length=20, blank=True, null=True)
    status_novo = models.CharField(max_length=20, blank=True, null=True)
    motivo_baixa = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='historicos_patrimonio'
    )
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']
        verbose_name = 'Histórico de Patrimônio'
        verbose_name_plural = 'Históricos de Patrimônio'

    def __str__(self):
        return f"{self.patrimonio.numero} - {self.get_tipo_movimento_display()} ({self.data:%d/%m/%Y %H:%M})"
