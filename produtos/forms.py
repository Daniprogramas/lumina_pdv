from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "descricao", "preco", "quantidade", "ativo", "categoria", "codigo_barras"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "preco": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "quantidade": forms.NumberInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "codigo_barras": forms.TextInput(attrs={"class": "form-control"}),
        }
