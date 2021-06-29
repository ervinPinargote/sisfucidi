from django import forms
from .models import Programa, Materia, Valor_matricula, CnotasEstudiante


class ProgramaNuevo(forms.ModelForm):
    class Meta:
        model = Programa
        fields = [
            'cod_programa',
            'nombre_programa',
            'duracion',
            'tipo_programa',
            #  'precio_matricula',
            #  'precio_pension',
            'vigencia',
        ]
        labels = {
            'cod_programa': 'Codigo Programa',
            'nombre_programa': 'Descripcion',
            'duracion': 'Duracion',
            'tipo_programa': 'Modalidad',
            # 'precio_matricula':'Valor Matricula',
            # 'precio_pension':'Valor Colegiatura',
            'vigencia': 'Vigencia',
        }
        codigo = Programa.objects.last()
        generado = "P" + str(codigo.id + 1)
        widgets = {
            'cod_programa': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_programa': forms.TextInput(attrs={'class': 'form-control'}),
            'duracion': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_programa': forms.Select(attrs={'class': 'form-control'}),
            # 'precio_matricula':forms.NumberInput(attrs={'class':'form-control'}),
            # 'precio_pension':forms.NumberInput(attrs={'class':'form-control'}),
            # 'vigencia':forms.BooleanField(required=True),
            'vigencia': forms.NullBooleanSelect(attrs={'class': 'form-control'}),
        }


class ProgramaEditar(forms.ModelForm):
    class Meta:
        model = Programa
        fields = [
            'cod_programa',
            'nombre_programa',
            'duracion',
            'tipo_programa',
            # 'precio_matricula',
            # 'precio_pension',
            'vigencia',
        ]
        labels = {
            'cod_programa': 'Codigo Programa',
            'nombre_programa': 'Descripcion',
            'duracion': 'Duracion',
            'tipo_programa': 'Modalidad',
            # 'precio_matricula':'Valor Matricula',
            # 'precio_pension':'Valor Colegiatura',
            'vigencia': 'Vigencia',
        }

        widgets = {
            'cod_programa': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'nombre_programa': forms.TextInput(attrs={'class': 'form-control'}),
            'duracion': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_programa': forms.Select(attrs={'class': 'form-control'}),
            # 'precio_matricula':forms.NumberInput(attrs={'class':'form-control'}),
            # 'precio_pension':forms.NumberInput(attrs={'class':'form-control'}),
            'vigencia': forms.NullBooleanSelect(attrs={'class': 'form-control'}),
        }


class MateriaNuevo(forms.ModelForm):
    class Meta:
        model = Materia
        fields = [
            'cod_programa',
            'cod_materia',
            'nombre_materia',
            'modalidad',
            'duracion',
            'estado',
            'nivel',
            'valor_presencial',
            'valor_online',
            'materia_id',
        ]
        labels = {
            'cod_programa': 'Codigo Programa',
            'cod_materia': 'Codigo Materia',
            'nombre_materia': 'Descripcion',
            'modalidad': 'Modalidad',
            'duracion': 'Duracion',
            'estado': 'Vigencia',
            'nivel': 'Nivel',
        }

        widgets = {
            'cod_programa': forms.Select(attrs={'class': 'form-control'}),
            'cod_materia': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_materia': forms.TextInput(attrs={'class': 'form-control'}),
            'modalidad': forms.Select(attrs={'class': 'form-control'}),
            'duracion': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_presencial': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_online': forms.NumberInput(attrs={'class': 'form-control'}),
            'nivel': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.NullBooleanSelect(attrs={'class': 'form-control'}),
            'materia_id': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class MateriaEditar(forms.ModelForm):
    class Meta:
        model = Materia
        fields = [
            'cod_programa',
            'cod_materia',
            'nombre_materia',
            'modalidad',
            'duracion',
            'estado',
            'nivel',
        ]
        labels = {
            'cod_programa': 'Codigo Programa',
            'cod_materia': 'Codigo Materia',
            'nombre_materia': 'Descripcion',
            'modalidad': 'Modalidad',
            'duracion': 'Duracion',
            'estado': 'Vigencia',
            'nivel': 'Nivel',
        }

        widgets = {
            'cod_programa': forms.Select(attrs={'class': 'form-control', 'readonly': True}),
            'cod_materia': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'nombre_materia': forms.TextInput(attrs={'class': 'form-control'}),
            'modalidad': forms.Select(attrs={'class': 'form-control'}),
            'duracion': forms.NumberInput(attrs={'class': 'form-control'}),
            'nivel': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.NullBooleanSelect(attrs={'class': 'form-control'}),
        }


class ValoresMatriculaForm(forms.ModelForm):
    class Meta:
        model = Valor_matricula
        fields = [
            'fecha',
            'valor_matricula_presencial',
            'valor_matricula_online',
            'cod_programa',
        ]
        labels = {
            'fecha': 'Fecha',
            'valor_matricula_presencial': 'Matricula Presencial',
            'valor_matricula_online': 'Matricula Online',
            'cod_programa': 'Programa de estudio',
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control'}),
            'valor_matricula_presencial': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_matricula_online': forms.NumberInput(attrs={'class': 'form-control'}),
            'cod_programa': forms.Select(attrs={'class': 'form-control'}),
        }


class NotaEstuForm(forms.ModelForm):
    class Meta:
        model = CnotasEstudiante
        fields = [
            'fecha_subir_nota',
            'notaestudiante',
            'asitencia',
        ]
        labels = {
            'fecha_subir_nota': 'Fecha',
            'notaestudiante': 'Nota',
            'asitencia': 'Asistencia',
        }
        widgets = {
            'fecha_subir_nota': forms.DateInput(attrs={'class': 'form-control', 'min': '2017-04-01', 'max': '2022-12-31' }),
            'notaestudiante': forms.NumberInput(attrs={'class': 'form-control'}),
            'asitencia': forms.NumberInput(attrs={'class': 'form-control'}),
        }
