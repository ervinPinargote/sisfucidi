from django.db import models


# Create your models here.

class Programa(models.Model):
    opciones = (
        ('N', 'No definido'),
        ('A', 'Anual'),
        ('M', 'Mensual'),
    )

    cod_programa = models.CharField(max_length=10, null=False, verbose_name="Codigo Prograna", unique=True)
    nombre_programa = models.CharField(max_length=70, null=False, verbose_name="Programa")
    duracion = models.IntegerField(verbose_name="Duracion")
    tipo_programa = models.CharField(max_length=10, default=None, choices=opciones, verbose_name="Modalidad Programa")
    # precio_matricula = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Valor Matricula",default=None)
    # precio_pension = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Valor Pension",default=None)
    vigencia = models.BooleanField()

    def __str__(self):
        return '{}'.format(self.nombre_programa)


class Valor_matricula(models.Model):
    fecha = models.DateField(
        verbose_name="Fecha Asignada")  # solo se Permite una Fecha unica para los valores no se puede repetir en la tabal
    valor_matricula_presencial = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Matricula ",
                                                     default=None)
    valor_matricula_online = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Valor Matricula",
                                                 default=None)
    cod_programa = models.ForeignKey('Programa', on_delete=models.CASCADE, verbose_name="Codigo Prograna")
    # 001 12/04/2021  25.00 15.00 PA  order_by (desc).top(1)
    # 002 15/04/2021  25.00 10.00 PA


class Materia(models.Model):
    opcionesM = (
        ('C', 'Creditos'),
        ('H', 'Horas'),
    )
    nivels = (
        (1, 'Uno'),
        (2, 'Dos'),
        (3, 'Tres'),
    )
    materia_id = models.IntegerField(null=False)
    cod_programa = models.ForeignKey('Programa', on_delete=models.CASCADE, verbose_name="Codigo Prograna")
    cod_materia = models.CharField(max_length=10, verbose_name="Codigo Asignatura", primary_key=True)
    nombre_materia = models.CharField(max_length=70, null=False, verbose_name="Asignatura")
    modalidad = models.CharField(max_length=10, choices=opcionesM)
    duracion = models.IntegerField(null=False)
    nivel = models.IntegerField(null=True, blank=True, choices=nivels, default=0)
    valor_presencial = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Presencial ")
    valor_online = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Online")
    estado = models.BooleanField()

    def __unicode__(self):
        return self.Programa.cod_programa

    def __str__(self):
        return '{}'.format(self.nombre_materia)


class CnotasEstudiante(models.Model):
    fecha_subir_nota = models.DateField(verbose_name="Fecha Nota")
    notaestudiante = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Nota")
    asitencia = models.IntegerField()
    id_pago_materia = models.ForeignKey('Pago.Pago', on_delete=models.CASCADE, verbose_name="Id_materia_recibir")
    # id del pago que se genero con esa orden de pago
