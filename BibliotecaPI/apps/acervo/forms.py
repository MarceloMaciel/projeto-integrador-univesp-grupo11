from django import forms

from .models import Exemplar


class ExemplarForm(forms.ModelForm):
    class Meta:
        model = Exemplar
        fields = [
            'livro',
            'codigo_tombo',
            'codigo_barras_interno',
            'localizacao_fisica',
            'status',
            'data_aquisicao',
            'observacoes',
            'lote_cadastro',
        ]
        widgets = {
            'data_aquisicao': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs.setdefault('class', 'form-select')
            else:
                field.widget.attrs.setdefault('class', 'form-control')
