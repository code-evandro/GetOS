from django.contrib import admin
from django.urls import path, include
from core import views as core_views  # Importa views da dashboard, menu, logout
from django.views.generic import RedirectView  # Importa para redirecionamento

urlpatterns = [
    path('admin/', admin.site.urls),

    # Páginas principais
    path('menu/', core_views.menu, name='menu'),
    path('dashboard/', core_views.dashboard, name='dashboard'),
    path('sair/', core_views.logout_redirect, name='logout_redirect'),

    # Apps do sistema
    path('setores/', include('setores.urls')),
    path('servidores/', include('servidores.urls')),
    path('ordens/', include('ordens.urls')),

    # Redirecionamento da raiz para o login
    path('', RedirectView.as_view(url='/login/', permanent=False)),

    # Autenticação padrão do Django
    path('', include('django.contrib.auth.urls')),
]
