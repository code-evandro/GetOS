from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_ordem, name='abrir_os'),
    path('visualizar/', views.visualizar_os, name='visualizar_os'),
    path('finalizar/<int:os_id>/', views.finalizar_os, name='finalizar_os'),  
    path('pdf/<int:id>/', views.gerar_pdf_os, name='gerar_pdf_os'),
    path('info-servidor/<int:servidor_id>/', views.info_servidor, name='info_servidor'),
]
