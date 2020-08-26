from django.db import models

# Create your models here.

class  Programa(models.Model):
    opciones = (
        ('N','No definido'),
        ('A', 'Anual'),
        ('M', 'Mensual'),
    )

    cod_programa = models.CharField(max_length=10, null=False, verbose_name="Codigo Prograna")
    nombre_programa = models.CharField(max_length=70,null = False,verbose_name="Programa")
    duracion = models.IntegerField(verbose_name="Duracion")
    tipo_programa = models.CharField(max_length=10, default=None,choices=opciones, verbose_name="Modalidad Programa")
    precio_matricula = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Valor Matricula",default=None)
    precio_pension = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Valor Pension",default=None)
    vigencia = models.BooleanField()

    def __str__(self):
        return '{}'.format(self.nombre_programa)

class Materia(models.Model):
    opcionesM = (
        ('C', 'Creditos'),
        ('H', 'Horas'),
    )


    cod_programa = models.ForeignKey('Programa',on_delete=models.CASCADE, verbose_name="Codigo Prograna")
    cod_materia = models.CharField(max_length=10,verbose_name="Codigo Asignatura", primary_key=True)
    nombre_materia = models.CharField(max_length=70, null=False, verbose_name="Asignatura")
    modalidad = models.CharField(max_length=10,choices=opcionesM)
    duracion = models.IntegerField(null=False)
    estado = models.BooleanField()

    def __unicode__(self):
        return self.Programa.cod_programa


