# Generated by Django 3.0.8 on 2021-04-27 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Matricula', '0003_auto_20210426_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='matricula',
            name='valor_pagar',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Valor a pagar'),
        ),
    ]
