from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_produtos, name="lista_produtos"),
    path("novo/", views.novo_produto, name="novo_produto"),
    path("<int:id>/", views.detalhe_produto, name="detalhe_produto"),
    path("<int:id>/editar/", views.editar_produto, name="editar_produto"),
    path("<int:id>/excluir/", views.excluir_produto, name="excluir_produto"),
]
