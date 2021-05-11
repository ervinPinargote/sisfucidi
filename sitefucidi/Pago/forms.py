from django import forms

from .models import detalle_pagos


class DetallesPagosForm(forms.ModelForm):
    class Meta:
        model = detalle_pagos
        fields = [
            'fecha',
            'valor_cancelado',
            'Valor_pendiente',
            'evidencia',
            'pago_id',
        ]
        labels = {
            'fecha': 'Fecha' ,
            'valor_cancelado': 'Matricula Presencial',
            'Valor_pendiente':'Matricula Online',
            'evidencia':'Comprobante de pago',
            'pago_id':'Referencia del pago',
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'class':'form-control'}),
            'valor_cancelado':forms.NumberInput(attrs={'class':'form-control'}),
            'Valor_pendiente':forms.NumberInput(attrs={'class':'form-control'}),
            'evidencia':forms.FileInput(attrs={'class':'form-control'}),
            'pago_id':forms.Select(attrs={'class':'form-control'}),
        }