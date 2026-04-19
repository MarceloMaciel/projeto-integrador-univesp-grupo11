from django.contrib import admin

from .models import Livro, LoteCadastro


admin.site.site_header = 'Biblioteca PI'
admin.site.site_title = 'Biblioteca PI'
admin.site.index_title = 'Administração da biblioteca'


@admin.register(LoteCadastro)
class LoteCadastroAdmin(admin.ModelAdmin):
    list_display = ('nota_fiscal', 'quantidade', 'usuario', 'data_hora_cadastro')
    search_fields = ('nota_fiscal', 'usuario__username')
    list_filter = ('data_hora_cadastro',)
    autocomplete_fields = ('usuario',)
    date_hierarchy = 'data_hora_cadastro'
    list_per_page = 25


@admin.register(Livro)
class LivroLegadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'autor', 'categoria', 'classificacao', 'usuario', 'lote', 'data_cadastro')
    list_filter = ('categoria', 'classificacao', 'data_cadastro')
    search_fields = ('nome', 'autor', 'codigo_barras')
    autocomplete_fields = ('usuario', 'lote')
    date_hierarchy = 'data_cadastro'
    list_per_page = 25
