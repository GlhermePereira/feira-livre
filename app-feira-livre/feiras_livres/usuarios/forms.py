# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UsuarioCreateForm(UserCreationForm):
    nome_completo = forms.CharField(
        max_length=150,
        label="Nome completo",
        widget=forms.TextInput(attrs={'placeholder': 'Ex: João da Silva'})
    )
    email = forms.EmailField(max_length=100, required=True, label="E-mail")
    telefone = forms.CharField(max_length=15, required=False, label="Telefone")
    
    cep = forms.CharField(max_length=9, required=False, label="CEP", widget=forms.TextInput(attrs={
        'onblur': 'buscarEnderecoPorCEP()',
        'placeholder': 'Ex: 11700000'
    }))
    rua = forms.CharField(max_length=100, required=False, label="Rua")
    numero = forms.CharField(max_length=10, required=False, label="Número")
    bairro = forms.CharField(max_length=100, required=False, label="Bairro")
    cidade = forms.CharField(max_length=100, required=False, label="Cidade")
    estado = forms.CharField(max_length=2, required=False, label="Estado")

    password1 = forms.CharField(
        label="Senha", 
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite uma senha segura'}),
        min_length=6,
        max_length=20
    )
    password2 = forms.CharField(
        label="Confirmar Senha", 
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita a senha'}),
        max_length=20
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        nome = self.cleaned_data.get('nome_completo', '').strip()
        nomes = nome.split(' ', 1)
        user.first_name = nomes[0]
        user.last_name = nomes[1] if len(nomes) > 1 else ''
        if commit:
            user.save()
        return user

    class Meta:
        model = Usuario
        fields = [
            'nome_completo', 'email', 'telefone',
            'cep', 'rua', 'numero', 'bairro', 'cidade', 'estado',
            'password1', 'password2'
        ]
