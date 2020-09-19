from django import forms

from .models import Persona, Experencia_espiritual, Trasfondo_eclesiastico, estudios_realizado, recomendaciones, \
    admisione


class PersonaForm(forms.ModelForm): # clase para el formulario de las personas.
    class Meta:
        model = Persona
        fields =[
            'ci',
            'nombre',
            'apellido',
            'pais',
            'provincia',
            'ciudad',
            'direccion',
            'tipo',
            'estado_c',
            'fecha_nacimiento',
            'edad',
            'telefono',
            'celular',
            'correo',
            'cal_Emer',
            'emer_tele',
            'estado',
        ]
        labels = {
            'ci': 'Cedula/Pasaporte',
            'nombre': 'Nombres',
            'apellido': 'Apellidos',
            'pais': 'Pais Residencia',
            'provincia':'Provincia',
            'ciudad':'Ciudad',
            'direccion':'Direccion',
            'tipo':'Tipo Registro',
            'estado_c':'Estado Civil',
            'fecha_nacimiento':'Fecha Nacimiento',
            'edad':'Edad',
            'telefono':'Telefono',
            'celular':'Celular',
            'correo':'Correo Electronico',
            'cal_Emer': 'Emergencia Nombre',
            'emer_tele':'Emergencia Celular',
            'estado':'Activo',
        }
        widgets = {
            'ci': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'provincia': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'value':'Estudiante','disabled':'True'}),
            'estado_c': forms.Select(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'cal_Emer': forms.TextInput(attrs={'class': 'form-control'}),
            'emer_tele': forms.TextInput(attrs={'class': 'form-control'}),
             'estado':forms.Select(attrs={'class': 'form-control'}),
        }

class ExpereciaForm(forms.ModelForm):
    class Meta:
        model = Experencia_espiritual
        fields =[
            'fecha_conversion',
            'fecha_bautismo',
            'bautismo_espiritual',
            'fecha_bautismo_es',
            'obra_señor',
            'desc_obra',
            'doctrinas',
            'opinion',
            'contribucion',
            'motivacion',
        ]
        labels = {
            'fecha_conversion':'Fecha de Conversion',
            'fecha_bautismo':'Fecha de Baustismo Agua',
            'bautismo_espiritual': '¿Tiene Bautismo Espiritual?',
            'fecha_bautismo_es':'Fecha Bautismo Espiritual',
            'obra_señor': '¿Tiene Obras hacia el Señor?',
            'desc_obra':'Descripcion',
            'doctrinas':'¿Tiene Doctrinas?',
            'opinion':'Opinion',
            'contribucion':'Contribucion',
            'motivacion':'Motivacion',
        }
        widgets = {
            'fecha_conversion': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            #'bautismo_espiritual':
            'fecha_bautismo': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'fecha_bautismo_es': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
           # 'obra_señor':
            'desc_obra': forms.TextInput(attrs={'class': 'form-control'}),
            #'doctrinas':
            'opinion': forms.TextInput(attrs={'class': 'form-control'}),
            'contribucion': forms.TextInput(attrs={'class': 'form-control'}),
            'motivacion': forms.TextInput(attrs={'class': 'form-control'}),
             # 'vigencia':forms.BooleanField(required=True),
        }

class TrasfondoForm(forms.ModelForm):
    class Meta:
        model = Trasfondo_eclesiastico
        fields=[
            'iglesia',
            'denominacion',
            'direcion',
            'miembro',
            'fecha_menbresia',
            'cargo_desempeñado',
            'nom_apellido',
        ]
        labes={
            'iglesia':'Iglesia Pertenece',
            'denominacion': 'Denominacion',
            'direcion':'Direccion Iglesia',
            'miembro':'¿Es Miembro?',
            'fecha_menbresia':'Fecha de Menbresia',
            'cargo_desempeñado': 'Cargo Desempeñado',
            'nom_apellido':'Nombre y apellido pastor',
        }
        widgets = {
        'iglesia': forms.TextInput(attrs={'class': 'form-control'}),
        'denominacion': forms.TextInput(attrs={'class': 'form-control'}),
        'direcion': forms.TextInput(attrs={'class': 'form-control'}),
        # 'miembro':
        'fecha_menbresia': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
        'cargo_desempeñado': forms.TextInput(attrs={'class': 'form-control'}),
        'nom_apellido': forms.TextInput(attrs={'class': 'form-control'}),
        }

class estudiosForm(forms.ModelForm):
    class Meta:
        model = estudios_realizado
        fields = [
            'tipo_est',
            'fecha_ini',
            'fecha_fin',
            'institucion',
            'graduacion',
        ]
        labels={
            'tipo_est' : 'Tipo de Estudios',
            'fecha_ini': 'Fecha Inicio',
            'fecha_fin': 'Fecha Fin',
            'institucion': 'Institucion',
            'graduacion' : 'Graduacion'
        }
        widgets={
            'tipo_est': forms.Select(attrs={'class':'form-control'}),
            'fecha_ini':forms.DateInput(attrs={'class':'form-control'}),
            'fecha_fin':forms.DateInput(attrs={'class':'form-control'}),
            'institucion':forms.TextInput(attrs={'class':'form-control'}),
            #'graduacion'
        }

class recomendacionesForm(forms.ModelForm):
    class Meta:
        model = recomendaciones
        fields = [
            'nombre_apellido',
            'direccion',
            'telefono',

        ]
        labels={
            'nombre_apellido' : 'Nombres y Apellidos',
            'direccion': 'Direccion',
            'telefono': 'Telefono',

        }
        widgets={
            'nombre_apellido': forms.TextInput(attrs={'class':'form-control'}),
            'direccion':forms.TextInput(attrs={'class':'form-control'}),
            'telefono':forms.TextInput(attrs={'class':'form-control'}),
        }

class admisioneForm(forms.ModelForm):
    class Meta:
        model = admisione
        fields = [
            'codigoAdmision',
            'Programa',
            'fecha',
            'foto',
            'id_requisito'
           # 'id_estudios'
        ]
        labels={
            'codigoAdmision':'Codigo Admision',
            'Programa': 'Programa Estudios',
            'fecha':'Fecha Admision',
            'foto': 'Foto Estudiante',
            'id_requisito':'Requisitos',
           # 'id_estudios':'Estudios Relaizados',

        }
        widgets={
            'codigoAdmision' : forms.TextInput(attrs={'class':'form-control'}),
            'Programa' : forms.Select(attrs={'class':'form-control'}),
            'fecha': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'foto':forms.FileInput(attrs={'class':'form-control','accept':'image/*'}),
            'id_requisito':forms.CheckboxSelectMultiple(),

        }

