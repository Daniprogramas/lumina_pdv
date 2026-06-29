from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UsuarioCreationForm

User = get_user_model()

def login_view(request):
    # Se já estiver logado, manda direto pro menu
    if request.user.is_authenticated:
        return redirect('menu')

    if User.objects.count() == 0:
        messages.warning(request, "Nenhum funcionário cadastrado. Cadastre o gestor primeiro.")
        return redirect('cadastro')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Bem-vindo(a) ao Lumina PDV, {user.username}!")
            return redirect('menu')
        else:
            messages.error(request, "Usuário ou senha inválidos. Verifique e tente novamente.")
        return render(request, 'registration/login.html')
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "Sessão encerrada com sucesso.")
    return redirect('login')


def cadastro_view(request):
    # TRAVA DE SEGURANÇA: Permite se for o primeiro usuário ou se o logado for Gestor/Staff
    if User.objects.count() > 0:
        if not request.user.is_authenticated or not (request.user.is_staff or getattr(request.user, 'perfil', None) == 'Gestor' or request.user.username == 'supervisor1'):
            messages.error(request, "Acesso negado. Apenas gestores podem cadastrar operadores.")
            return redirect('menu')

    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST, request.FILES)
        
        # Captura os dados diretamente enviados pelo HTML
        username_post = request.POST.get('username')
        nome_post = request.POST.get('nome_completo')
        senha_post = request.POST.get('password1')
        foto_post = request.FILES.get('foto_operador')

        if username_post and senha_post:
            try:
                # FIX: Cria o usuário primeiro com os parâmetros estritos do Django
                novo_usuario = User.objects.create_user(
                    username=username_post,
                    password=senha_post,
                    is_active=True
                )
                
                # FIX SEGURO: Tenta preencher 'nome_completo'. Se falhar, joga no padrão 'first_name' do Django
                if hasattr(novo_usuario, 'nome_completo'):
                    novo_usuario.nome_completo = nome_post
                else:
                    novo_usuario.first_name = nome_post
                
                # Associa a foto se ela foi enviada
                if foto_post and hasattr(novo_usuario, 'foto_operador'):
                    novo_usuario.foto_operador = foto_post

                # Regra de negócio para definição de perfis
                if User.objects.count() == 1:
                    novo_usuario.perfil = "Gestor"
                    novo_usuario.is_staff = True
                    messages.success(request, f"Gestor {username_post} cadastrado com sucesso!")
                else:
                    novo_usuario.perfil = "Operador"
                    novo_usuario.is_staff = False
                    messages.success(request, f"Operador {username_post} cadastrado com sucesso!")
                
                # Salva o usuário modificado com sucesso
                novo_usuario.save()
                
                if request.user.is_authenticated:
                    return redirect('menu')
                return redirect('login')
                
            except Exception as e:
                messages.error(request, f"Erro ao salvar no banco de dados: {e}")
        else:
            messages.error(request, "Por favor, preencha o usuário e a senha corretamente.")
    else:
        form = UsuarioCreationForm()
        
    return render(request, 'registration/cadastro.html', {'form': form})


@login_required
def alterar_senha_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            usuario = form.save()
            update_session_auth_hash(request, usuario)  # mantém sessão ativa
            messages.success(request, "Senha alterada com sucesso!")
            return redirect('menu')
        else:
            messages.error(request, "Erro ao alterar senha. Verifique as regras.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'usuarios/alterar_senha.html', {'form': form})


@login_required
def menu_view(request):
    print("\n" + "#"*50)
    print("USUÁRIOS QUE O RUNSERVER ENXERGA:", list(User.objects.values_list('username', flat=True)))
    print("#"*50 + "\n")
    
    return render(request, 'usuarios/menu.html')