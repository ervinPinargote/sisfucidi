# Generated by Django 3.0.8 on 2021-04-21 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academico', '0016_auto_20210420_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='materia',
            name='valor_online',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=6, verbose_name='Valor Matricula'),
        ),
        migrations.AddField(
            model_name='materia',
            name='valor_presencial',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=6, verbose_name='Matricula '),
        ),
    ]
