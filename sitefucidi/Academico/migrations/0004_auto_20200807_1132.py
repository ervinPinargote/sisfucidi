# Generated by Django 3.0.8 on 2020-08-07 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academico', '0003_auto_20200807_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programa',
            name='tipo',
            field=models.CharField(choices=[('A', 'Anual'), ('M', 'Mensual')], default='N/D', max_length=10, null=True),
        ),
    ]