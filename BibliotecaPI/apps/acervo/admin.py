from django.contrib import admin

from .models import Exemplar


@admin.register(Exemplar)
class ExemplarAdmin(admin.ModelAdmin):
    list_display = ('codigo_tombo', 'livro', 'status', 'localizacao_fisica', 'data_aquisicao', 'lote_cadastro')
    list_filter = ('status', 'localizacao_fisica', 'data_aquisicao')
    search_fields = ('codigo_tombo', 'codigo_barras_interno', 'livro__titulo', 'livro__isbn')
    autocomplete_fields = ('livro', 'lote_cadastro')
    readonly_fields = ('criado_em',)
    list_per_page = 25
