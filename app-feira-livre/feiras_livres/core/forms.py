from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UsuarioCreateForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True)
    telefone = forms.CharField(max_length=15, required=False)
    endereco = forms.CharField(widget=forms.Textarea, required=False)
    password1 = forms.CharField(
        label="Senha", 
        widget=forms.PasswordInput,
        min_length=6,
        max_length=20
    )
    password2 = forms.CharField(
        label="Confirmar Senha", 
        widget=forms.PasswordInput,
        max_length=20
    )

    class Meta:  # agora está corretamente indentada
        model = Usuario
        fields = ['username', 'email', 'telefone', 'endereco', 'password1', 'password2']
