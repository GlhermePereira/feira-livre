from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
Usuario = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    is_staff = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'email', 'first_name', 'last_name', 'telefone', 'endereco', 'password', 'is_staff']

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise DRFValidationError(e.messages)
        return value

    def create(self, validated_data):
        return Usuario.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            telefone=validated_data.get('telefone', ''),
            endereco=validated_data.get('endereco', ''),
            password=validated_data['password'],
            is_staff=validated_data.get('is_staff', False),
        )




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # ESSENCIAL: define o campo que será usado para login
    username_field = Usuario.USERNAME_FIELD  # retorna 'email'

    def validate(self, attrs):
        # aqui pega o campo correto (email)
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if not all(credentials.values()):
            raise serializers.ValidationError(_("Preencha todos os campos."), code='authorization')

        user = authenticate(request=self.context.get('request'), **credentials)

        if not user:
            raise serializers.ValidationError(_("E-mail ou senha incorretos."), code='authorization')

        data = super().validate(attrs)

        # opcional: adiciona dados extras no payload do token
        data['email'] = user.email
        data['nome'] = user.first_name
        return data
