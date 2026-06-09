from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Patrimonio, HistoricoPatrimonio
from .forms import (
    PatrimonioForm,
    TransferenciaSetorForm,
    TransferenciaResponsavelForm,
    BaixaPatrimonioForm,
    PatrimonioFilterForm,
)


def _registrar_historico(patrimonio, tipo, descricao, usuario, **kwargs):
    """Utilitário para criar registro no histórico."""
    HistoricoPatrimonio.objects.create(
        patrimonio=patrimonio,
        tipo_movimento=tipo,
        descricao=descricao,
        usuario=usuario,
        **kwargs
    )


@login_required
def cadastrar_patrimonio(request):
    form = PatrimonioForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            patrimonio = form.save(commit=False)
            patrimonio.save()

            _registrar_historico(
                patrimonio=patrimonio,
                tipo=HistoricoPatrimonio.TipoMovimento.CRIACAO,
                descricao=f'Patrimônio {patrimonio.numero} cadastrado.',
                usuario=request.user,
                setor_novo=patrimonio.setor.nome,
                responsavel_novo=patrimonio.responsavel.get_full_name() or patrimonio.responsavel.username,
                status_novo=patrimonio.get_status_display(),
            )

            messages.success(
                request,
                f'Patrimônio {patrimonio.numero} cadastrado com sucesso!'
            )
            return redirect('patrimonio_detalhes', id=patrimonio.id)
        else:
            messages.error(request, 'Preencha todos os campos corretamente.')

    return render(request, 'getos/cad_patrimonio.html', {'form': form})


@login_required
def listar_patrimonios(request):
    patrimonios = Patrimonio.objects.filter(ativo=True).select_related('setor', 'responsavel')
    filter_form = PatrimonioFilterForm(request.GET or None)

    if filter_form.is_valid():
        setor = filter_form.cleaned_data.get('setor')
        status = filter_form.cleaned_data.get('status')
        busca = filter_form.cleaned_data.get('busca')

        if setor:
            patrimonios = patrimonios.filter(setor=setor)
        if status:
            patrimonios = patrimonios.filter(status=status)
        if busca:
            patrimonios = patrimonios.filter(
                Q(numero__icontains=busca) | Q(descricao__icontains=busca)
            )

    patrimonios = patrimonios.order_by('numero')

    return render(request, 'getos/listar_patrimonios.html', {
        'patrimonios': patrimonios,
        'filter_form': filter_form,
    })


@login_required
def detalhes_patrimonio(request, id):
    patrimonio = get_object_or_404(
        Patrimonio.objects.select_related('setor', 'responsavel'),
        id=id,
        ativo=True
    )
    historico = patrimonio.historico.select_related('usuario').all()

    return render(request, 'getos/detalhes_patrimonio.html', {
        'patrimonio': patrimonio,
        'historico': historico,
    })


@login_required
def transferir_setor(request, id):
    patrimonio = get_object_or_404(Patrimonio, id=id, ativo=True)

    if patrimonio.status == Patrimonio.Status.BAIXADO:
        messages.error(request, 'Não é possível transferir patrimônio baixado.')
        return redirect('patrimonio_detalhes', id=patrimonio.id)

    form = TransferenciaSetorForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            novo_setor = form.cleaned_data['setor']
            setor_anterior = patrimonio.setor.nome

            if novo_setor == patrimonio.setor:
                messages.warning(request, 'O novo setor é igual ao atual.')
            else:
                patrimonio.setor = novo_setor
                patrimonio.save()

                _registrar_historico(
                    patrimonio=patrimonio,
                    tipo=HistoricoPatrimonio.TipoMovimento.TRANSFERENCIA_SETOR,
                    descricao=f'Transferência de setor: {setor_anterior} → {novo_setor.nome}',
                    usuario=request.user,
                    setor_anterior=setor_anterior,
                    setor_novo=novo_setor.nome,
                )

                messages.success(
                    request,
                    f'Setor transferido com sucesso para {novo_setor.nome}.'
                )
                return redirect('patrimonio_detalhes', id=patrimonio.id)

    return render(request, 'getos/transferir_setor.html', {
        'form': form,
        'patrimonio': patrimonio,
    })


@login_required
def transferir_responsavel(request, id):
    patrimonio = get_object_or_404(Patrimonio, id=id, ativo=True)

    if patrimonio.status == Patrimonio.Status.BAIXADO:
        messages.error(request, 'Não é possível transferir patrimônio baixado.')
        return redirect('patrimonio_detalhes', id=patrimonio.id)

    form = TransferenciaResponsavelForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            novo_responsavel = form.cleaned_data['responsavel']
            responsavel_anterior_nome = (
                patrimonio.responsavel.get_full_name()
                or patrimonio.responsavel.username
            )
            novo_responsavel_nome = (
                novo_responsavel.get_full_name()
                or novo_responsavel.username
            )

            if novo_responsavel == patrimonio.responsavel:
                messages.warning(request, 'O novo responsável é igual ao atual.')
            else:
                patrimonio.responsavel = novo_responsavel
                patrimonio.save()

                _registrar_historico(
                    patrimonio=patrimonio,
                    tipo=HistoricoPatrimonio.TipoMovimento.TRANSFERENCIA_RESPONSAVEL,
                    descricao=f'Transferência de responsável: {responsavel_anterior_nome} → {novo_responsavel_nome}',
                    usuario=request.user,
                    responsavel_anterior=responsavel_anterior_nome,
                    responsavel_novo=novo_responsavel_nome,
                )

                messages.success(
                    request,
                    f'Responsável transferido com sucesso para {novo_responsavel_nome}.'
                )
                return redirect('patrimonio_detalhes', id=patrimonio.id)

    return render(request, 'getos/transferir_responsavel.html', {
        'form': form,
        'patrimonio': patrimonio,
    })


@login_required
def baixar_patrimonio(request, id):
    patrimonio = get_object_or_404(Patrimonio, id=id, ativo=True)

    if patrimonio.status == Patrimonio.Status.BAIXADO:
        messages.warning(request, 'Este patrimônio já está baixado.')
        return redirect('patrimonio_detalhes', id=patrimonio.id)

    form = BaixaPatrimonioForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            motivo = form.cleaned_data['motivo']
            status_anterior = patrimonio.get_status_display()

            patrimonio.status = Patrimonio.Status.BAIXADO
            patrimonio.save()

            _registrar_historico(
                patrimonio=patrimonio,
                tipo=HistoricoPatrimonio.TipoMovimento.BAIXA,
                descricao=f'Patrimônio baixado. Motivo: {motivo}',
                usuario=request.user,
                status_anterior=status_anterior,
                status_novo=patrimonio.get_status_display(),
                motivo_baixa=motivo,
            )

            messages.success(
                request,
                f'Patrimônio {patrimonio.numero} baixado com sucesso.'
            )
            return redirect('patrimonio_detalhes', id=patrimonio.id)
        else:
            messages.error(request, 'O motivo da baixa é obrigatório.')

    return render(request, 'getos/baixar_patrimonio.html', {
        'form': form,
        'patrimonio': patrimonio,
    })


@login_required
def alterar_status(request, id):
    patrimonio = get_object_or_404(Patrimonio, id=id, ativo=True)

    if patrimonio.status == Patrimonio.Status.BAIXADO:
        messages.error(request, 'Não é possível alterar o status de patrimônio baixado.')
        return redirect('patrimonio_detalhes', id=patrimonio.id)

    if request.method == 'POST':
        novo_status = request.POST.get('status')
        if novo_status in dict(Patrimonio.Status.choices):
            status_anterior = patrimonio.get_status_display()
            patrimonio.status = novo_status
            patrimonio.save()

            _registrar_historico(
                patrimonio=patrimonio,
                tipo=HistoricoPatrimonio.TipoMovimento.ALTERACAO_STATUS,
                descricao=f'Status alterado: {status_anterior} → {patrimonio.get_status_display()}',
                usuario=request.user,
                status_anterior=status_anterior,
                status_novo=patrimonio.get_status_display(),
            )

            messages.success(request, 'Status alterado com sucesso.')
        else:
            messages.error(request, 'Status inválido.')

        return redirect('patrimonio_detalhes', id=patrimonio.id)

    return render(request, 'getos/alterar_status.html', {
        'patrimonio': patrimonio,
        'status_choices': Patrimonio.Status.choices,
    })
