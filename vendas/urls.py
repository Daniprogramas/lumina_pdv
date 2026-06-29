from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_vendas_view, name="lista_vendas"),
    path("registrar/", views.registrar_venda_view, name="nova_venda"),
    path("remover-item/<int:item_id>/", views.remover_item_view, name="remover_item"),
    path("recibo/<int:venda_id>/", views.recibo_venda_view, name="recibo_venda"),
    path("detalhe/<int:venda_id>/", views.detalhe_venda_view, name="detalhe_venda"),
    path('recibo/<int:venda_id>/', views.recibo_venda_view, name='recibo_venda'),

]
