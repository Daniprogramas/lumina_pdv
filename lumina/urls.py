"""
URL configuration for lumina project.
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Função simples para redirecionar quem entrar na raiz direto para a sua rota de login
def redirecionar_para_login(request):
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Quando entrar em http://127.0.0.1:8000/, joga para a sua view de login
    path('', redirecionar_para_login, name='home'),  
    
    # ATENÇÃO: Removemos o prefixo 'usuarios/' para que as suas rotas fiquem limpas na raiz!
    # Agora a sua rota será /login/ e /menu/ ao invés de /usuarios/login/
    path('', include('usuarios.urls')),
    
    # Seus outros apps continuam perfeitos aqui
    path('produtos/', include('produtos.urls')),
    path('vendas/', include('vendas.urls')),
]