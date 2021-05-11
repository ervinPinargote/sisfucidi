
from django import forms

from .models import Matricula


class cMatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields=[
            'cod_matricula',
            'admision_id',
            'fecha_matricula',
            'modalidad',
            'id_matricula',
            'porcentaje_beca',
            'extesion',
            'valor_pagar',
        ]
        labes={
            'cod_matricula':'Codigo Matricula',
            'admision_id': 'Codigo Admision',
            'fecha_matricula':'Fecha Matricula',
            'modalidad': 'Modalidad',
        }
        widgets = {
        'cod_matricula': forms.TextInput(attrs={'class': 'form-control'}),
        'admision_id': forms.Select(attrs={'class': 'form-control'}),
        'id_matricula':forms.NumberInput(attrs={'class':'form-control'}),
        'fecha_matricula': forms.SelectDateWidget(attrs={'class': 'form-control', 'style':'width:auto; display: inline;'}),
        'modalidad': forms.Select(attrs={'class':'form-control'}),
        'porcentaje_beca':forms.NumberInput(attrs={'class':'form-control'}),
        'extesion':  forms.TextInput(attrs={'class': 'form-control'}),
        'valor_pagar'  : forms.NumberInput(attrs={'class':'form-control'}),
        }