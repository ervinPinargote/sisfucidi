# Generated by Django 3.0.8 on 2021-04-27 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academico', '0023_materia_materia_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materia',
            name='materia_id',
            field=models.IntegerField(),
        ),
    ]
