from django.db import models

# Create your models here.

class Persona(models.Model):
    opciones = (
        ('Instructor','Instructor'),
        ('Estudiante','Estudiante'),
        ('Administrativo', 'Administrativo'),
    )
    estado = (
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    )
    estado_civil = (
        ('Soltero(a)', 'Soltero(a)'),
        ('Casado(a)', 'Casado(a)'),
        ('Divorciado(a)', 'Divorciado(a)'),
        ('Viudo(a)', 'Viudo(a)'),
    )

    ci = models.CharField(max_length=10,primary_key=True,null=False,verbose_name="Documento Identidad")
    nombre = models.CharField(max_length=60,null = False)
    apellido = models.CharField(max_length=60,null = False)
    pais = models.CharField(max_length=20, verbose_name="Pais",null=True)
    provincia = models.CharField(max_length=20, verbose_name="Provincia",null=True)
    ciudad = models.CharField(max_length=20, verbose_name="Ciudad",null=True)
    direccion = models.CharField(max_length=50)
    tipo = models.CharField(max_length=15, default=None, choices=opciones, verbose_name="Tipo Persona")
    estado_c = models.CharField(max_length=15,default=None, choices=estado_civil,verbose_name="Estado Civil")
    fecha_nacimiento = models.DateField()
    edad = models.IntegerField(default=0,null=True)
    telefono = models.CharField(max_length=14,null = True)
    celular = models.CharField(max_length=14, null=True)
    correo = models.EmailField(default=None)
    cal_Emer = models.CharField(max_length=30, null=True, default="None")
    emer_tele = models.CharField(max_length=15,null=True, default="0900000000")
    estado = models.CharField(max_length=10, default=None, choices=estado, verbose_name="Estado")
    def __str__(self):
        return self.ci

# Requisitos que debe llevar una Solicitud de admision.
class Requisito(models.Model):
    codigo = models.CharField(max_length=10,null=False,verbose_name="Codigo Requisito")
    descripcion = models.CharField(max_length=100,null=False,verbose_name="Descripcion")

#apartado de Experiencia Espiritual
class Experencia_espiritual(models.Model):
    fecha_conversion = models.DateField(verbose_name="Fecha de Conversion") #fecha de conversion de la persona
    fecha_bautismo = models.DateField(verbose_name="Fecha Bautismo Agua")  # fecha de bautismo de la persona
    bautismo_espiritual = models.BooleanField(verbose_name="Bautismo Espiritual")  # ¿has recibido Bautismo del espitiru Santo? si/no
    fecha_bautismo_es = models.DateField(verbose_name="Bautismo Espiritual", null=True) # Fecha Bautismo Esperitual
    obra_señor = models.BooleanField(verbose_name="Llamamiento Obra Señor") #¿Tienes llamamiento a la obra del señor? si/no
    desc_obra = models.CharField(verbose_name="Obra Señor",max_length=100,null=True) #Descripcion a la obra del señor
    doctrinas = models.BooleanField(verbose_name="Doctrinas de Iglesia") # Conoce doctrinas de la iglesia del Dios.
    opinion = models.CharField(verbose_name="Necesidad Principal",max_length=100,null=True) # Necesidades Pincipales de la iglesia de hoy ?
    contribucion = models.CharField(verbose_name="Contribucion", max_length=100,null=True)  # Contribucion Necesidades Pincipales de la iglesia de hoy ?
    motivacion = models.CharField(verbose_name="Motivacion", max_length=100,null=True)  # Motivacion Ingresar a Seminarios.

# apartado de Trasfondo eclesiastico
class Trasfondo_eclesiastico(models.Model):
    iglesia= models.CharField(verbose_name="Iglesia Perteneciente", null=True, max_length=100) # ¿A que iglesia Pertenece?
    denominacion = models.CharField(verbose_name="Denominacion", null=True, max_length=100) # Denominacion
    direcion = models.CharField(verbose_name="Direccion Iglesia", null=True, max_length=200) # Direccion Iglesia, en el formulario considerar Calle, Canton, Provincia
    miembro = models.BooleanField(verbose_name="Miembro") # ¿Eres mienbro?
    fecha_menbresia = models.DateField(verbose_name="Fecha Menbresia",null=True)
    cargo_desempeñado = models.CharField(verbose_name="Cargos Desempeñados",null=True, max_length=200)
    nom_apellido = models.CharField(verbose_name="Nombre y Apellido Pastor", null=True, max_length=70)

#aparatado de estudos realizados
class estudios_realizado(models.Model):
    opciones = (
        ('Primarios', 'Primarios'),
        ('Secundarios', 'Secundarios'),
        ('Universitarios', 'Universitarios'),
        ('Religiosos', 'Religiosos'),
        ('Otros', 'Otros'),
    )

    tipo=models.CharField(verbose_name="Tipo Estutdios", choices=opciones,max_length=20,null=True)
    fecha_ini = models.DateField(verbose_name="Fecha Inicio",null=True)
    fecha_fin = models.DateField(verbose_name ="Fecha Final",null=True)
    institucion = models.CharField(verbose_name="Nombre Institucion",null=True, max_length=100)
    graduacion = models.BooleanField(verbose_name="Graduacion")
    ci = models.ForeignKey('Persona', on_delete=models.CASCADE, verbose_name="Estudio de")

# aparatado de Recomendaciones
class recomendaciones(models.Model):
    nombre_apellido = models.CharField(verbose_name="Nombre y Apellidos",null=True,max_length=70)
    direccion = models.CharField(verbose_name="Direccion Domicilio", null=True, max_length=100)
    telefono = models.CharField(verbose_name="telefono", null=True,max_length=11)
    ci = models.ForeignKey('Persona', on_delete=models.CASCADE, verbose_name="Referencia de")

class admisione(models.Model):
    codigoAdmision = models.CharField(verbose_name="Codigo de Admision", null=False,max_length=10)
    ci = models.ForeignKey('Persona', on_delete=models.CASCADE, verbose_name="Cedula Admision")
    id_ex = models.ForeignKey('Experencia_espiritual', on_delete=models.CASCADE, verbose_name="Id  Experiencia")
    id_tra = models.ForeignKey('Trasfondo_eclesiastico',on_delete=models.CASCADE, verbose_name="Id Transfondo")
    id_requisito = models.ManyToManyField('Requisito')
    id_estudios = models.ManyToManyField('estudios_realizado')
    id_refecencia = models.ManyToManyField('recomendaciones')
    Programa = models.ForeignKey('Academico.Programa',blank=True,null=False,default=1,on_delete=models.CASCADE,verbose_name="Programa Estudiar")
    fecha = models.DateField(verbose_name="Fecha Solicitud",null=True)
    foto = models.ImageField(upload_to='admision_images',null=True,blank=True)


#class admisione_requisito(models.Model):
#    id = models.AutoField()
#    id_admision = models.ForeignKey('admisione',primary_key=True,on_delete=models.CASCADE)
#    id_requisto = models.ForeignKey('Requisito',primary_key=True,on_delete=models.CASCADE)

#class  admisione_estudio(models.Model):
#    id = models.AutoField()
#    id_admision = models.ForeignKey('admisione',primary_key=True,on_delete=models.CASCADE)
#    id_estudios = models.ForeignKey('estudios_realizado',primary_key=True,on_delete=models.CASCADE)

#class admisione_referencia(models.Model):
#    id = models.AutoField()
#    id_admision = models.ForeignKey('admisione', primary_key=True,on_delete=models.CASCADE)
#    id_refecencia = models.ForeignKey('recomendaciones', primary_key=True,on_delete=models.CASCADE)



















