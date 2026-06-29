from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    # Adicionando explicitamente os campos que seu HTML usa
    nome_completo = forms.CharField(
        max_length=150, 
        required=True, 
        label="Nome Completo"
    )
    foto_operador = forms.ImageField(
        required=False, 
        label="Foto do Operador"
    )
    perfil = forms.ChoiceField(
        choices=[("Gestor", "Gestor"), ("Operador", "Operador")],
        label="Perfil de Acesso",
        required=False
    )
    ativo = forms.BooleanField(
        initial=True, 
        required=False, 
        label="Usuário Ativo",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input', 
            'style': 'transform: scale(1.5); cursor: pointer;'
        })
    )

    class Meta:
        model = Usuario
        # IMPORTANTE: Incluir todos os campos que trafegam no HTML e no modelo
        fields = ("username", "email", "nome_completo", "perfil", "ativo", "foto_operador")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Injeta as classes do seu CSS/Bootstrap em todos os campos, exceto no checkbox
        for field_name, field in self.fields.items():
            if field_name != 'ativo':
                field.widget.attrs['class'] = 'form-control form-control-lg border-2'
                if field.label:
                    field.widget.attrs['placeholder'] = f'INSIRA O {field.label.upper()}'