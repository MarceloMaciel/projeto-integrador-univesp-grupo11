from django.db import models


class Exemplar(models.Model):
    class Status(models.TextChoices):
        DISPONIVEL = 'DISPONIVEL', 'Disponível'
        EMPRESTADO = 'EMPRESTADO', 'Emprestado'
        RESERVADO = 'RESERVADO', 'Reservado'
        MANUTENCAO = 'MANUTENCAO', 'Manutenção'

    livro = models.ForeignKey('catalogo.Livro', on_delete=models.CASCADE, related_name='exemplares', verbose_name='Livro')
    codigo_tombo = models.CharField(max_length=50, unique=True, verbose_name='Código de patrimônio/tombo')
    codigo_barras_interno = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Código de barras interno',
    )
    localizacao_fisica = models.CharField(max_length=150, verbose_name='Localização física')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DISPONIVEL, db_index=True, verbose_name='Situação')
    data_aquisicao = models.DateField(null=True, blank=True, verbose_name='Data de aquisição')
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    lote_cadastro = models.ForeignKey(
        'core.LoteCadastro',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='exemplares',
        verbose_name='Lote de cadastro',
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        ordering = ['codigo_tombo']
        verbose_name = 'Exemplar'
        verbose_name_plural = 'Exemplares'
        indexes = [
            models.Index(fields=['codigo_tombo']),
            models.Index(fields=['status']),
            models.Index(fields=['localizacao_fisica']),
        ]

    def __str__(self):
        return f'{self.codigo_tombo} - {self.livro.titulo}'
