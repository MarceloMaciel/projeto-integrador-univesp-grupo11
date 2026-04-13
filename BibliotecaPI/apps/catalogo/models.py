from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Autor(models.Model):
    nome = models.CharField(max_length=180, unique=True, verbose_name='Nome')
    nacionalidade = models.CharField(max_length=100, blank=True, verbose_name='Nacionalidade')
    data_nascimento = models.DateField(null=True, blank=True, verbose_name='Data de nascimento')

    class Meta:
        ordering = ['nome']
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def __str__(self):
        return self.nome


class Editora(models.Model):
    nome = models.CharField(max_length=180, unique=True, verbose_name='Nome')
    cidade = models.CharField(max_length=120, blank=True, verbose_name='Cidade')

    class Meta:
        ordering = ['nome']
        verbose_name = 'Editora'
        verbose_name_plural = 'Editoras'

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    nome = models.CharField(max_length=120, unique=True, verbose_name='Nome')
    descricao = models.TextField(blank=True, verbose_name='Descrição')

    class Meta:
        ordering = ['nome']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome


class Livro(models.Model):
    isbn_validator = RegexValidator(
        regex=r'^[0-9Xx\-]{10,17}$',
        message='Informe um ISBN válido (10 a 17 caracteres, com números, X e hífen).',
    )

    titulo = models.CharField(max_length=220, verbose_name='Título')
    subtitulo = models.CharField(max_length=220, blank=True, verbose_name='Subtítulo')
    isbn = models.CharField(max_length=17, unique=True, validators=[isbn_validator], verbose_name='ISBN')
    ano_publicacao = models.PositiveIntegerField(
        validators=[MinValueValidator(1450), MaxValueValidator(2100)],
        verbose_name='Ano de publicação',
    )
    edicao = models.CharField(max_length=50, blank=True, verbose_name='Edição')
    resumo = models.TextField(blank=True, verbose_name='Resumo')
    capa = models.ImageField(upload_to='capas/', null=True, blank=True, verbose_name='Capa')
    autores = models.ManyToManyField(Autor, related_name='livros', verbose_name='Autores')
    editora = models.ForeignKey(
        Editora,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='livros',
        verbose_name='Editora',
    )
    categorias = models.ManyToManyField(Categoria, related_name='livros', blank=True, verbose_name='Categorias')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['titulo']
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
        indexes = [
            models.Index(fields=['titulo']),
            models.Index(fields=['isbn']),
            models.Index(fields=['ano_publicacao']),
        ]

    def __str__(self):
        return f'{self.titulo} ({self.isbn})'

    @property
    def titulo_completo(self) -> str:
        if self.subtitulo:
            return f'{self.titulo}: {self.subtitulo}'
        return self.titulo
