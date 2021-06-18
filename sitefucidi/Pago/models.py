from django.db import models
from django.utils.html import escape

# Create your models here.



class Pago(models.Model):
    opciones = (
        ('Matricula', 'Matricula'),
        ('Colegiatura', 'Colegiatura'),
    )
    cod_matricula = models.ForeignKey('Matricula.Matricula',on_delete=models.CASCADE,verbose_name="Codigo Matricula" )
    cod_pago= models.CharField(max_length=10,verbose_name="Codigo Pago",null=False)
    descripcion = models.CharField(max_length=20,default=None,choices=opciones)
    obervaciones = models.CharField(max_length=100)
    fecha_generacion = models.DateField(verbose_name="Fecha Creado",default=None)
    valor_pagar = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Valor a Pagar",default=0.0)
    valor_pagado = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Valor a Pagar", default=0.0)
    estado = models.BooleanField(verbose_name="Estado")



class detalle_pagos(models.Model):
    fecha = models.DateField(verbose_name="Fecha Pago",default=None)
    valor_cancelado = models.DecimalField(max_digits=6, decimal_places=2,verbose_name="Valor Cancelado", default=0.0)
    Valor_pendiente = models.DecimalField(max_digits=6, decimal_places=2,verbose_name="Valor Pendiente", default=0.0)
    evidencia = models.ImageField(upload_to="pagos/matricula",verbose_name="Respaldo",null=True,default=None)
    pago_id = models.ForeignKey('Pago', on_delete=models.CASCADE, verbose_name="id_pago")

class materia_recibir(models.Model):
    fecha = models.DateField(verbose_name="Fecha Pago",default=None)
    materia_asignada = models.ForeignKey('Academico.Materia',on_delete=models.CASCADE, verbose_name="id_Materia")
    pago_id = models.ForeignKey('Pago', on_delete=models.CASCADE, verbose_name="id_pago")