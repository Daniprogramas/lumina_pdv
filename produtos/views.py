from django.shortcuts import render, get_object_or_404, redirect
from .models import Produto
from .forms import ProdutoForm
from django.contrib import messages  # Importação necessária para as mensagens de confirmação

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, "produtos/list.html", {"produtos": produtos})

def detalhe_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, "produtos/detalhe_produtos.html", {"produto": produto})

def novo_produto(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro de produto realizado com sucesso!")
            return redirect("lista_produtos")
    else:
        form = ProdutoForm()
    return render(request, "produtos/create.html", {"form": form})

def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado com sucesso!")
            return redirect("lista_produtos")
    else:
        form = ProdutoForm(instance=produto)
    return render(request, "produtos/edit.html", {"form": form, "produto": produto})

def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == "POST":
        produto.delete()
        messages.success(request, "Produto deletado com sucesso!")
        return redirect("lista_produtos")
    return render(request, "produtos/delete.html", {"produto": produto})
