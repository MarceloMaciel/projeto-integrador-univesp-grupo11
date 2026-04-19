from django.contrib.auth.models import User
from django.db import models


class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    matricula = models.CharField(max_length=20, unique=True, verbose_name='Matrícula')
    precisa_trocar_senha = models.BooleanField(default=True, verbose_name='Precisa trocar senha')

    class Meta:
        verbose_name = 'Perfil de usuário'
        verbose_name_plural = 'Perfis de usuários'

    def __str__(self):
        return f'{self.user.username} - {self.matricula}'


class LoteCadastro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lotes_cadastrados', verbose_name='Usuário')
    nota_fiscal = models.CharField(max_length=100, verbose_name='Número da nota fiscal')
    quantidade = models.PositiveIntegerField(verbose_name='Quantidade de livros')
    data_hora_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data e hora do cadastro')

    class Meta:
        verbose_name = 'Lote de cadastro'
        verbose_name_plural = 'Lotes de cadastro'
        ordering = ['-data_hora_cadastro']

    def __str__(self):
        return f'NF {self.nota_fiscal} - {self.quantidade} livro(s)'


class Livro(models.Model):
    CATEGORIAS = (
        ('FIC', 'Ficção'),
        ('MIST', 'Mistério'),
        ('ROM', 'Romance'),
        ('TEC', 'Tecnologia'),
        ('OUT', 'Outros'),
    )

    CLASSIFICACAO = (
        (1, '1 estrela'),
        (2, '2 estrelas'),
        (3, '3 estrelas'),
        (4, '4 estrelas'),
        (5, '5 estrelas'),
    )

    nome = models.CharField(max_length=200, verbose_name='Nome do livro')
    autor = models.CharField(max_length=150, verbose_name='Autor')
    codigo_barras = models.CharField(max_length=50, unique=True, verbose_name='Código de barras')
    categoria = models.CharField(max_length=4, choices=CATEGORIAS, verbose_name='Categoria')
    classificacao = models.IntegerField(choices=CLASSIFICACAO, verbose_name='Classificação')
    lote = models.ForeignKey(
        LoteCadastro,
        on_delete=models.CASCADE,
        related_name='livros_legado',
        null=True,
        blank=True,
        verbose_name='Lote',
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='livros_cadastrados', verbose_name='Usuário')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro')

    class Meta:
        verbose_name = 'Livro (legado por lote)'
        verbose_name_plural = 'Livros (legado por lote)'
        ordering = ['-data_cadastro']

    def __str__(self):
        return self.nome
