from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

Usuario = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    is_staff = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'email', 'first_name', 'last_name', 'telefone', 'endereco', 'password', 'is_staff']

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
