from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acervo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exemplar',
            name='status',
            field=models.CharField(
                choices=[
                    ('DISPONIVEL', 'Disponível'),
                    ('EMPRESTADO', 'Emprestado'),
                    ('RESERVADO', 'Reservado'),
                ],
                default='DISPONIVEL',
                max_length=20,
            ),
        ),
    ]
