# Generated by Django 3.0.8 on 2020-09-18 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academico', '0012_auto_20200826_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='materia',
            name='nivel',
            field=models.IntegerField(blank=True, choices=[(1, 'Uno'), (2, 'Dos'), (3, 'Tres')], default=0, null=True),
        ),
    ]