from django.contrib import admin
from .models import Feira, Barraca, PresencaBarracaFeira

@admin.register(Feira)
class FeiraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'bairro', 'cidade', 'ativa')
    list_filter = ('dias_funcionamento', 'ativa')
    search_fields = ('nome', 'bairro', 'cidade')
    ordering = ('nome',)

@admin.register(Barraca)
class BarracaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'feira', 'feirante')
    search_fields = ('nome', 'descricao')
    autocomplete_fields = ['feira', 'feirante']

@admin.register(PresencaBarracaFeira)
class PresencaAdmin(admin.ModelAdmin):
    list_display = ('barraca', 'feira', 'data')
    list_filter = ('data',)
