# Generated by Django 3.0.8 on 2021-04-21 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academico', '0020_auto_20210421_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materia',
            name='valor_online',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=6, verbose_name='Online'),
        ),
        migrations.AlterField(
            model_name='materia',
            name='valor_presencial',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=6, verbose_name='Presencial '),
        ),
    ]
