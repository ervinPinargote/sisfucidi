from django.db import models

# Create your models here.
class Matricula(models.Model):
    opciones = (
        ('Presencial', 'Presencial'),
        ('Online', 'Online'),
    )
    cod_matricula = models.CharField(primary_key=True,verbose_name="Codigo Matricula",max_length=10,default=None)
    cod_programa = models.ForeignKey('Academico.Programa', on_delete=models.CASCADE, verbose_name="Codigo Programa")
    ci = models.ForeignKey('Admision.Persona',on_delete=models.CASCADE,verbose_name="Codigo Estudiante")
    fecha_matricula = models.DateField(null=False)
    nivel = models.IntegerField()
    modalidad = models.CharField(max_length=15,choices=opciones,default=None)
    def __str__(self):
        return self.cod_matricula















