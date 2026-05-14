from uuid import uuid4

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acervo', '0002_alter_exemplar_status'),
        ('circulacao', '0002_remove_auditoria'),
    ]

    operations = [
        # Novos campos na Reserva
        migrations.AddField(
            model_name='reserva',
            name='exemplar',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='reservas',
                to='acervo.exemplar',
                verbose_name='Exemplar separado',
            ),
        ),
        migrations.AddField(
            model_name='reserva',
            name='protocolo',
            field=models.CharField(
                blank=True,
                max_length=24,
                null=True,
                unique=True,
                verbose_name='Protocolo',
            ),
        ),
        migrations.AddField(
            model_name='reserva',
            name='tipo',
            field=models.CharField(
                choices=[('FILA', 'Fila de espera'), ('RETIRADA', 'Retirada no balcão')],
                db_index=True,
                default='FILA',
                max_length=20,
                verbose_name='Tipo',
            ),
        ),
        # Alterar ordenação padrão para FIFO
        migrations.AlterModelOptions(
            name='reserva',
            options={
                'ordering': ['data_reserva', 'id'],
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
            },
        ),
        # Constraint: um usuário só pode ter uma reserva ativa por livro
        migrations.AddConstraint(
            model_name='reserva',
            constraint=models.UniqueConstraint(
                condition=models.Q(status='ATIVA'),
                fields=['livro', 'usuario'],
                name='unique_reserva_ativa_por_livro_usuario',
            ),
        ),
    ]
