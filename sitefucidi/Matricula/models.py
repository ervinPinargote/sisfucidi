from django.db import models

# Create your models here.
class Matricula(models.Model):
    opciones = (
        ('Presencial', 'Presencial'),
        ('Online', 'Online'),
    )
    id_matricula = models.IntegerField(null=False) # sirve para generar el codigo de matricula
    cod_matricula = models.CharField(primary_key=True,verbose_name="Codigo Matricula",max_length=10,default=None)
    admision_id = models.ForeignKey('Admision.admisione', on_delete=models.CASCADE, verbose_name="Admisione")
    fecha_matricula = models.DateField(null=False,default=None)
    modalidad = models.CharField(max_length=15,choices=opciones,default=None)
    porcentaje_beca = models.IntegerField(null=False, default= 0) # para indicar el Porcentaje de descauento por beca
    extesion = models.CharField(max_length=50,default=None)
    valor_pagar = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="Valor a pagar")

    def __str__(self):
        return self.cod_matricula












