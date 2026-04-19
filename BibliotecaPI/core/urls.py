from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trocar-senha/', views.trocar_senha, name='trocar_senha'),
    path('iniciar-lote/', views.iniciar_lote_cadastro, name='iniciar_lote_cadastro'),
    path('cadastrar-livro/', views.cadastrar_livro_lote, name='cadastrar_livro_lote'),
]
