
from django import forms

from .models import Matricula


class cMatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields=[
            'cod_matricula',
            'admision_id',
            'materias',
            'fecha_matricula',
            'nivel',
            'modalidad',
        ]
        labes={
            'cod_matricula':'Codigo Matricula',
            'admision_id': 'Codigo Admision',
            'materias':'Lista de Materias',
            'fecha_matricula':'Fecha Matricula',
            'nivel':'Nivel',
            'modalidad': 'Modalidad',
        }
        widgets = {
        'cod_matricula': forms.TextInput(attrs={'class': 'form-control'}),
        'admision_id': forms.Select(attrs={'class': 'form-control'}),
        'materias': forms.CheckboxSelectMultiple(attrs={'class':'QuitarPuntos'}),
        'fecha_matricula': forms.SelectDateWidget(attrs={'class': 'form-control', 'style':'width:auto; display: inline;'}),
        'nivel': forms.NumberInput(attrs={'class':'form-control'}),
        'modalidad': forms.Select(attrs={'class':'form-control'}),
        }