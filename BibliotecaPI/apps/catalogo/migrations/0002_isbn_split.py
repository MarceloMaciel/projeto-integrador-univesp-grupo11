"""
Migration: isbn → isbn_10 + isbn_13

Estratégia segura para banco já existente (PostgreSQL/Render):
1. Adiciona isbn_10 e isbn_13 como nullable/sem unique ainda
2. Copia o valor de isbn para o campo correto conforme comprimento
3. Remove a coluna isbn original
4. Aplica unique constraint em isbn_10 e isbn_13 separadamente
"""
from django.db import migrations, models


def copiar_isbn(apps, schema_editor):
    Livro = apps.get_model('catalogo', 'Livro')
    for livro in Livro.objects.exclude(isbn='').exclude(isbn__isnull=True):
        isbn = livro.isbn.strip().replace('-', '') if livro.isbn else ''
        if not isbn:
            continue
        if len(isbn) == 10:
            livro.isbn_10 = isbn
        elif len(isbn) == 13:
            livro.isbn_13 = isbn
        else:
            # ISBN ambíguo: salva no campo 13 por ser mais comum
            livro.isbn_13 = isbn
        livro.save(update_fields=['isbn_10', 'isbn_13'])


def reverter_isbn(apps, schema_editor):
    Livro = apps.get_model('catalogo', 'Livro')
    for livro in Livro.objects.all():
        if livro.isbn_13:
            livro.isbn = livro.isbn_13
        elif livro.isbn_10:
            livro.isbn = livro.isbn_10
        livro.save(update_fields=['isbn'])


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0001_initial'),
    ]

    operations = [
        # 1. Adiciona os dois novos campos sem unique (para poder popular)
        migrations.AddField(
            model_name='livro',
            name='isbn_10',
            field=models.CharField(
                max_length=10,
                blank=True,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='livro',
            name='isbn_13',
            field=models.CharField(
                max_length=13,
                blank=True,
                null=True,
            ),
        ),
        # 2. Migra dados
        migrations.RunPython(copiar_isbn, reverter_isbn),
        # 3. Remove a coluna antiga
        migrations.RemoveField(
            model_name='livro',
            name='isbn',
        ),
        # 4. Aplica unique constraints
        migrations.AlterField(
            model_name='livro',
            name='isbn_10',
            field=models.CharField(
                max_length=10,
                unique=True,
                blank=True,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='livro',
            name='isbn_13',
            field=models.CharField(
                max_length=13,
                unique=True,
                blank=True,
                null=True,
            ),
        ),
    ]
