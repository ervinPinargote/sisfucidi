from django.db import models
from django.utils.html import escape

# Create your models here.



class Pago(models.Model):
    opciones = (
        ('Matricula', 'Matricula'),
        ('Colegiatura', 'Colegiatura'),
    )
    cod_matricula = models.ForeignKey('Matricula.Matricula',on_delete=models.CASCADE,verbose_name="Codigo Matricula" )
    estudiante = models.ForeignKey('Admision.Persona',on_delete=models.CASCADE,verbose_name="Codigo Estudiante")
    cod_pago= models.CharField(max_length=10,verbose_name="Codigo Pago",null=False)
    Descripcion = models.CharField(max_length=20,default=None,choices=opciones)
    obervaciones = models.CharField(max_length=100)
    evidencia = models.ImageField(upload_to='vaucher_pago',verbose_name="Escaneado Vaucher",null=True,default=None)
    estado = models.BooleanField(verbose_name="Estado del Pago")
    fecha_pago = models.DateField(verbose_name="Fecha Generado Pago",default=None)
    val = models.Field.get_prep_value(self='Matricula',value='valor')
    valor_pagar = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Valor a Pagar",default=None)
    Valor_pagado = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Valor Pagado",default=None)

    def image_tag(self):

        return u'<img src="%s" />' % escape( 'vaucher_pago')
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True