from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_setor, name='cad_setor'),
    path('listar/', views.listar_setores, name='listar_setores'),  # ✅ resolve o erro no menu
    path('editar/<int:id>/', views.editar_setor, name='editar_setor'),
]
