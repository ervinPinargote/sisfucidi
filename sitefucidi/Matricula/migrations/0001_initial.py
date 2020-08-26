# Generated by Django 3.0.8 on 2020-08-18 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Admision', '0001_initial'),
        ('Academico', '0011_auto_20200818_0948'),
    ]

    operations = [
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('cod_matricula', models.CharField(default=None, max_length=10, primary_key=True, serialize=False, verbose_name='Codigo Matricula')),
                ('fecha_matricula', models.DateField()),
                ('nivel', models.IntegerField()),
                ('modalidad', models.CharField(choices=[('Presencial', 'Presencial'), ('Online', 'Online')], default=None, max_length=15)),
                ('ci', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admision.Persona', verbose_name='Codigo Estudiante')),
                ('cod_programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academico.Programa', verbose_name='Codigo Programa')),
            ],
        ),
    ]