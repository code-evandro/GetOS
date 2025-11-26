from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_servidor, name='cad_servidor'),
    path('listar/', views.listar_servidores, name='listar_servidores'),  # ✅ essa rota resolve o erro do menu
    path('editar/<int:id>/', views.editar_servidor, name='editar_servidor'),
]
