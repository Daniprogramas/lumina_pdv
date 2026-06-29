from django import forms
from .models import Venda, ItemVenda

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ["cliente_nome", "forma_pagamento", "troco"]


class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ["produto", "quantidade"]

    def clean(self):
        cleaned_data = super().clean()
        produto = cleaned_data.get("produto")
        quantidade = cleaned_data.get("quantidade")

        if produto and quantidade:
            if quantidade > produto.estoque:
                raise forms.ValidationError("Quantidade maior que o estoque disponível.")
        return cleaned_data
