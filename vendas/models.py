from django.db import models
from django.utils import timezone
from usuarios.models import Usuario
from produtos.models import Produto

class Venda(models.Model):
    operador = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Operador")
    cliente_nome = models.CharField(max_length=100, verbose_name="Cliente")
    data_venda = models.DateTimeField(default=timezone.now, verbose_name="Data da Venda")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor Total")
    forma_pagamento = models.CharField(max_length=50, verbose_name="Forma de Pagamento", default="Dinheiro")
    troco = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Troco")

    def __str__(self):
        return f"Venda #{self.id} - Cliente: {self.cliente_nome} ({self.forma_pagamento})"


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def calcular_subtotal(self):
        self.subtotal = self.quantidade * self.preco_unitario
        return self.subtotal

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"
