# Generated by Django 3.0.8 on 2020-08-07 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Programa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_programa', models.CharField(max_length=10, verbose_name='Codigo Prograna')),
                ('nombre_programa', models.CharField(max_length=70, verbose_name='Programa')),
                ('duracion', models.IntegerField(verbose_name='Duracion * Años')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Valor')),
                ('vigencia', models.BooleanField()),
            ],
        ),
    ]
