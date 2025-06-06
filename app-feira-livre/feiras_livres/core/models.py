from django.db import models
from django.conf import settings  # Para acessar AUTH_USER_MODEL
from django.core.validators import RegexValidator


class Feira(models.Model):
    DIAS_CHOICES = [
        ('seg', 'Segunda-feira'),
        ('ter', 'Terça-feira'),
        ('qua', 'Quarta-feira'),
        ('qui', 'Quinta-feira'),
        ('sex', 'Sexta-feira'),
        ('sab', 'Sábado'),
        ('dom', 'Domingo'),
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome da Feira")
    endereco = models.TextField(verbose_name="Endereço Completo")
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50, default="Praia Grande")

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    dias_funcionamento = models.CharField(
        max_length=50,
        help_text="Separe os dias por vírgula (ex: seg,qua,sex)"
    )
    horario_abertura = models.TimeField()
    horario_fechamento = models.TimeField()

    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Feira"
        verbose_name_plural = "Feiras"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.bairro})"


class Barraca(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Barraca")
    feira = models.ForeignKey(Feira, on_delete=models.CASCADE, related_name="barracas")
    feirante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="barracas"
    )
    descricao = models.TextField(blank=True, verbose_name="Descrição")

    class Meta:
        verbose_name = "Barraca"
        verbose_name_plural = "Barracas"

    def __str__(self):
        return f"{self.nome} (Feira: {self.feira})"


class PresencaBarracaFeira(models.Model):
    feira = models.ForeignKey(Feira, on_delete=models.CASCADE)
    barraca = models.ForeignKey(Barraca, on_delete=models.CASCADE)
    data = models.DateField()

    local_mapa = models.CharField(max_length=100, blank=True)
    coordenadas = models.CharField(
        max_length=50,
        blank=True,
        help_text="Formato: 'latitude,longitude'"
    )

    class Meta:
        verbose_name = "Presença de Barraca"
        verbose_name_plural = "Presenças de Barracas"
        unique_together = ['feira', 'barraca', 'data']

    def __str__(self):
        return f"{self.barraca} em {self.feira} ({self.data})"
