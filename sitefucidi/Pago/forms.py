from django import forms

from .models import detalle_pagos, Pago, materia_recibir


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
            'fecha': 'Fecha',
            'valor_cancelado': 'Matricula Presencial',
            'Valor_pendiente': 'Matricula Online',
            'evidencia': 'Comprobante de pago',
            'pago_id': 'Referencia del pago',
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control'}),
            'valor_cancelado': forms.NumberInput(attrs={'class': 'form-control'}),
            'Valor_pendiente': forms.NumberInput(attrs={'class': 'form-control'}),
            'evidencia': forms.FileInput(attrs={'class': 'form-control'}),
            'pago_id': forms.Select(attrs={'class': 'form-control'}),
        }


class PagosForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = [
            'cod_matricula',
            'cod_pago',
            'descripcion',
            'obervaciones',
            'fecha_generacion',
            'valor_pagar',
            'valor_pagado',
            'estado',
        ]
        labels = {
            'cod_matricula':'codigo de matricula',
            'cod_pago':'codigo de pago',
            'descripcion': 'descripcion',
            'obervaciones': 'Observaciones',
            'fecha_generacion': 'Fecha de pago Generado',
            'valor_pagar': 'Valor a pagar',
            'valor_pagado': 'Valor pagado',
            'estado':'Estado',
        }
        widgets = {

            'cod_matricula': forms.Select(attrs={'class': 'form-control'}),
            'cod_pago': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'obervaciones': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_generacion': forms.DateInput(attrs={'class': 'form-control'}),
            'valor_pagar': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_pagado': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

class FormMateriaPago(forms.ModelForm):
    class Meta:
        model = materia_recibir
        fields = [
            'fecha',
            'materia_asignada',
            'pago_id',
        ]
        labels = {
            'fecha':'fecha',
            'materia_asignada':'Materia a Escoger',
            'pago_id': 'Referencia del pago',
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control'}),
            'materia_asignada': forms.Select(attrs={'class': 'form-control'}),
            'pago_id': forms.Select(attrs={'class': 'form-control'}),
        }