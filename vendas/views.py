import json  # Adicionado para ler a sacola vinda do JavaScript
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from .forms import VendaForm, ItemVendaForm
from .models import Venda, ItemVenda
from produtos.models import Produto  # Importa o modelo de Produtos para listagem e estoque
from usuarios.models import Usuario  # Importa seu modelo customizado para evitar o ValueError

@login_required
def detalhe_venda_view(request, venda_id):
    """ Exibe os detalhes de uma venda específica """
    venda = get_object_or_404(Venda, id=venda_id)
    return render(request, "vendas/detalhe_venda.html", {"venda": venda})

def lista_vendas_view(request):
    """ Lista todas as vendas realizadas e verifica se deve abrir o recibo por JS """
    vendas = Venda.objects.all().order_by("-data_venda")
    abrir_recibo_id = request.GET.get("abrir_recibo")
    
    return render(request, "vendas/list.html", {
        "vendas": vendas,
        "abrir_recibo_id": abrir_recibo_id
    })

@login_required
def registrar_venda_view(request):
    """ Processa a sacola de compras do PDV e registra a nova venda """
    if request.method == "POST":
        itens_sacola_json = request.POST.get("itens_sacola", "[]")
        nome_cliente = request.POST.get("nome_cliente", "Consumidor Final")
        forma_pagamento = request.POST.get("forma_pagamento", "Dinheiro")
        troco = request.POST.get("troco", "0.00")
        
        try:
            itens_sacola = json.loads(itens_sacola_json)
        except json.JSONDecodeError:
            itens_sacola = []

        if not itens_sacola:
            messages.error(request, "Não é possível registrar uma venda sem itens na sacola!")
            return redirect("nova_venda")

        # SOLUÇÃO DO OPERADOR: Captura o utilizador customizado diretamente da sessão atual da request
        usuario_logado = Usuario.objects.get(username=request.user.username)

        # Cria a venda principal vinculando o operador que está REALMENTE logado
        venda = Venda.objects.create(
            operador=usuario_logado,
            cliente_nome=nome_cliente,
            forma_pagamento=forma_pagamento,
            troco=float(troco.replace(",", ".")),
            valor_total=0.00
        )

        total_venda = 0.00

        for item_sacola in itens_sacola:
            produto = get_object_or_404(Produto, id=item_sacola["id"])
            quantidade = int(item_sacola["quantidade"])
            subtotal = float(produto.preco) * quantidade
            total_venda += subtotal

            ItemVenda.objects.create(
                venda=venda,
                produto=produto,
                quantidade=quantidade,
                preco_unitario=produto.preco,
                subtotal=subtotal
            )

            if hasattr(produto, 'estoque') and produto.estoque is not None:
                produto.estoque -= quantidade
                produto.save()

        venda.valor_total = total_venda
        venda.save()

        messages.success(request, f"Venda #{venda.id} realizada com sucesso!")
        return redirect(f"/vendas/?abrir_recibo={venda.id}")

    else:
        produtos = Produto.objects.all()
        ultima_venda = Venda.objects.last()
        proximo_numero_venda = (ultima_venda.id + 1) if ultima_venda else 1

    return render(request, "vendas/create.html", {
        "produtos": produtos,
        "proximo_numero_venda": proximo_numero_venda
    })

@login_required
def remover_item_view(request, item_id):
    item = get_object_or_404(ItemVenda, id=item_id)
    venda = item.venda
    item.delete()
    venda.valor_total = sum(i.subtotal for i in venda.itens.all())
    venda.save()
    messages.info(request, "Item removido da venda.")
    return redirect("lista_vendas")

@login_required
def recibo_venda_view(request, venda_id):
    """ Gera o arquivo PDF no estilo Cupom Fiscal de Supermercado (Bobina 80mm) """
    venda = get_object_or_404(Venda, id=venda_id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="cupom_venda_{venda.id}.pdf"'

    # Define o tamanho do papel estilo Cupom (Largura: 80mm ~ 226 pontos, Altura longa para caber tudo)
    largura_bobina = 226
    # Calcula a altura estimada com base na quantidade de itens para não cortar o papel
    altura_bobina = 350 + (venda.itens.count() * 25)
    
    p = canvas.Canvas(response, pagesize=(largura_bobina, altura_bobina))
    
    # Usamos a fonte Courier (monoespaçada) para dar o visual de impressora de cupom fiscal
    p.setFont("Courier-Bold", 10)

    # Início do topo da fita
    y = altura_bobina - 20
    
    p.drawCentredString(largura_bobina / 2, y, "LUMINA PDV LTDA")
    y -= 12
    p.setFont("Courier", 8)
    p.drawCentredString(largura_bobina / 2, y, "RUA DO MERCADO, 123 - CENTRO")
    y -= 15
    
    p.drawString(10, y, "----------------------------------")
    y -= 12
    p.setFont("Courier-Bold", 8)
    p.drawString(10, y, f"CUPOM FISCAL SIMULADO  NFP: {venda.id:06d}")
    y -= 12
    p.setFont("Courier", 8)
    p.drawString(10, y, f"DATA: {venda.data_venda.strftime('%d/%m/%Y %H:%M:%S')}")
    y -= 12
    p.drawString(10, y, f"OPERADOR: {venda.operador.username[:18].upper()}")
    y -= 12
    p.drawString(10, y, f"CLIENTE: {venda.cliente_nome[:20].upper()}")
    y -= 15
    
    p.drawString(10, y, "----------------------------------")
    y -= 12
    p.setFont("Courier-Bold", 8)
    p.drawString(10, y, "CÓD QTD   UN   DESCRIÇÃO         TOTAL")
    y -= 12
    p.setFont("Courier", 8)
    p.drawString(10, y, "----------------------------------")
    y -= 15

    # Listagem dos Itens comprados
    for i, item in enumerate(venda.itens.all(), start=1):
        # Quebra o nome do produto caso seja muito grande para a fita
        nome_prod = item.produto.nome[:18].upper()
        p.drawString(10, y, f"{i:03d} {item.quantidade:02d}   UN   {nome_prod}")
        # Alinha o valor do subtotal à direita da fita
        p.drawRightString(largura_bobina - 10, y, f"{item.subtotal:.2f}")
        y -= 14

    y -= 5
    p.drawString(10, y, "----------------------------------")
    y -= 15
    
    # Totais e Fechamento
    p.setFont("Courier-Bold", 10)
    p.drawString(10, y, "TOTAL R$")
    p.drawRightString(largura_bobina - 10, y, f"{venda.valor_total:.2f}")
    y -= 15
    
    p.setFont("Courier", 8)
    p.drawString(10, y, f"FORMA PAGTO: {venda.forma_pagamento.upper()}")
    y -= 12
    p.drawString(10, y, "TROCO R$")
    p.drawRightString(largura_bobina - 10, y, f"{venda.troco:.2f}")
    y -= 20
    
    p.drawString(10, y, "----------------------------------")
    y -= 12
    p.setFont("Courier-Oblique", 8)
    p.drawCentredString(largura_bobina / 2, y, "Obrigado pela preferência!")
    
    p.showPage()
    p.save()

    return response