from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sair/', views.logout_redirect, name='logout_redirect'),
]
