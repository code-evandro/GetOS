from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_patrimonio, name='patrimonio_cadastrar'),
    path('listar/', views.listar_patrimonios, name='patrimonio_listar'),
    path('<int:id>/', views.detalhes_patrimonio, name='patrimonio_detalhes'),
    path('<int:id>/transferir-setor/', views.transferir_setor, name='patrimonio_transferir_setor'),
    path('<int:id>/transferir-responsavel/', views.transferir_responsavel, name='patrimonio_transferir_responsavel'),
    path('<int:id>/baixar/', views.baixar_patrimonio, name='patrimonio_baixar'),
    path('<int:id>/alterar-status/', views.alterar_status, name='patrimonio_alterar_status'),
]
