from django.contrib import admin

from apps.acervo.models import Exemplar

from .models import Autor, Categoria, Editora, Livro


class ExemplarInline(admin.TabularInline):
    model = Exemplar
    fields = ('codigo_tombo', 'status', 'localizacao_fisica')
    extra = 0
    show_change_link = True


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nacionalidade', 'data_nascimento')
    list_filter = ('nacionalidade',)
    search_fields = ('nome', 'nacionalidade')
    list_per_page = 25


@admin.register(Editora)
class EditoraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade')
    list_filter = ('cidade',)
    search_fields = ('nome', 'cidade')
    list_per_page = 25


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    list_per_page = 25


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'isbn', 'ano_publicacao', 'editora', 'atualizado_em')
    list_filter = ('ano_publicacao', 'categorias')
    search_fields = ('titulo', 'subtitulo', 'isbn', 'autores__nome', 'editora__nome')
    filter_horizontal = ('autores', 'categorias')
    readonly_fields = ('criado_em', 'atualizado_em')
    inlines = (ExemplarInline,)
    list_per_page = 25
