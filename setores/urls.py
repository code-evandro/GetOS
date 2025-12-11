from django.urls import path 
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_setor, name='cad_setor'),
    path('listar/', views.listar_setores, name='listar_setores'),
    path('editar/<int:id>/', views.editar_setor, name='editar_setor'),

    # Rota de teste do novo layout
    path('teste-layout/', views.teste_layout, name='teste_layout'),
]
