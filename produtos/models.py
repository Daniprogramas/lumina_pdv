from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Produto")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    quantidade = models.PositiveIntegerField(default=0, verbose_name="Quantidade em Estoque")
    ativo = models.BooleanField(default=True, verbose_name="Disponível")

    # Campos adicionais do documento de requisitos
    categoria = models.CharField(
        max_length=50,
        choices=[
            ("comida_rapida", "Comida rápida"),
            ("bebida", "Bebida"),
            ("doces_salgados", "Doces / Salgados"),
            ("equipamentos", "Equipamentos"),
            ("jogos", "Jogos"),
            ("servicos", "Serviços de lan house"),
        ],
        default="servicos",
        verbose_name="Categoria"
    )
    codigo_barras = models.CharField(max_length=50, blank=True, null=True, verbose_name="Código de Barras")
    data_cadastro = models.DateField(auto_now_add=True, verbose_name="Data de Cadastro")

    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"
