from django import forms
from .models import Programa, Materia


class ProgramaNuevo(forms.ModelForm):

    class Meta:
        model = Programa
        fields = [
            'cod_programa',
            'nombre_programa',
            'duracion',
            'tipo_programa',
            'precio_matricula',
            'precio_pension',
            'vigencia',
        ]
        labels = {
            'cod_programa': 'Codigo Programa' ,
            'nombre_programa': 'Descripcion',
            'duracion':'Duracion',
            'tipo_programa':'Modalidad',
            'precio_matricula':'Valor Matricula',
            'precio_pension':'Valor Colegiatura',
            'vigencia':'Vigencia',
        }
        codigo = Programa.objects.last()
        generado =  "P"+str(codigo.id+1)
        widgets = {
            'cod_programa': forms.TextInput(attrs={'class':'form-control','value':generado}),
            'nombre_programa':forms.TextInput(attrs={'class':'form-control'}),
            'duracion':forms.NumberInput(attrs={'class':'form-control'}),
            'tipo_programa':forms.Select(attrs={'class':'form-control'}),
            'precio_matricula':forms.NumberInput(attrs={'class':'form-control'}),
            'precio_pension':forms.NumberInput(attrs={'class':'form-control'}),
            #'vigencia':forms.BooleanField(required=True),
        }

class ProgramaEditar(forms.ModelForm):

    class Meta:
        model = Programa
        fields = [
            'cod_programa',
            'nombre_programa',
            'duracion',
            'tipo_programa',
            'precio_matricula',
            'precio_pension',
            'vigencia',
        ]
        labels = {
            'cod_programa': 'Codigo Programa' ,
            'nombre_programa': 'Descripcion',
            'duracion':'Duracion',
            'tipo_programa':'Modalidad',
            'precio_matricula':'Valor Matricula',
            'precio_pension':'Valor Colegiatura',
            'vigencia':'Vigencia',
        }

        widgets = {
            'cod_programa': forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),
            'nombre_programa':forms.TextInput(attrs={'class':'form-control'}),
            'duracion':forms.NumberInput(attrs={'class':'form-control'}),
            'tipo_programa':forms.Select(attrs={'class':'form-control'}),
            'precio_matricula':forms.NumberInput(attrs={'class':'form-control'}),
            'precio_pension':forms.NumberInput(attrs={'class':'form-control'}),
            #'vigencia':forms.BooleanField(required=True),
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
        ]
        labels = {
            'cod_programa': 'Codigo Programa' ,
            'cod_materia': 'Codigo Materia',
            'nombre_materia':'Descripcion',
            'modalidad':'Modalidad',
            'duracion':'Duracion',
            'estado':'Vigencia',
        }

        widgets = {
            'cod_programa': forms.Select(attrs={'class':'form-control'}),
            'cod_materia':forms.TextInput(attrs={'class':'form-control'}),
            'nombre_materia':forms.TextInput(attrs={'class':'form-control'}),
            'modalidad':forms.Select(attrs={'class':'form-control'}),
            'duracion':forms.NumberInput(attrs={'class':'form-control'}),
            #'estado':forms.NumberInput(attrs={'class':'form-control'}),
            #'vigencia':forms.BooleanField(required=True),
        }