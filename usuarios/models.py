from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # Define as opções de perfil direto no banco de dados (Mais seguro)
    TIPO_PERFIL = (
        ("Gestor", "Gestor"),
        ("Operador", "Operador"),
    )
    
    perfil = models.CharField(max_length=50, choices=TIPO_PERFIL, default="Operador", verbose_name="Perfil")
    
    # CORREÇÃO PARA O ERRO DO DJANGO (fields.E304):
    # Adicionamos related_name exclusivo para não bater de frente com o User nativo
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )

    # NÃO precisamos recriar o campo 'ativo'. 
    # O AbstractUser já nos dá o campo 'is_active' nativamente!

    def autenticar(self):
        return self.is_authenticated

    def validar_permissao(self):
        # Valida se tem permissão administrativa baseado no perfil ou nas flags do Django
        return self.perfil == "Gestor" or self.is_staff or self.is_superuser

    class Meta:
        db_table = 'usuarios_usuario' # Força o Django a usar a tabela exata que você criou no MySQL