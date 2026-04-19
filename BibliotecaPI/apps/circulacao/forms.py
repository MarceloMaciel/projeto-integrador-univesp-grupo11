from django import forms
from django.utils import timezone

from apps.acervo.models import Exemplar

from .models import Emprestimo, Reserva


class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['exemplar', 'usuario', 'data_prevista_devolucao']
        widgets = {'data_prevista_devolucao': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exemplar'].queryset = Exemplar.objects.filter(status=Exemplar.Status.DISPONIVEL).select_related('livro')
        for field in self.fields.values():
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs.setdefault('class', 'form-select')
            else:
                field.widget.attrs.setdefault('class', 'form-control')

    def clean_data_prevista_devolucao(self):
        data = self.cleaned_data['data_prevista_devolucao']
        if data <= timezone.localdate():
            raise forms.ValidationError('A data prevista deve ser posterior a hoje.')
        return data


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['livro', 'data_expiracao']
        widgets = {'data_expiracao': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs.setdefault('class', 'form-select')
            else:
                field.widget.attrs.setdefault('class', 'form-control')

    def clean_data_expiracao(self):
        data_expiracao = self.cleaned_data.get('data_expiracao')
        if data_expiracao and data_expiracao < timezone.localdate():
            raise forms.ValidationError('Data de expiração inválida.')
        return data_expiracao


class DevolucaoForm(forms.Form):
    data_devolucao = forms.DateField(
        label='Data de devolução',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
    )

    def __init__(self, *args, emprestimo=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.emprestimo = emprestimo

    def clean_data_devolucao(self):
        data = self.cleaned_data.get('data_devolucao')
        data = data or timezone.localdate()
        if data > timezone.localdate():
            raise forms.ValidationError('A data de devolução não pode ser futura.')
        if self.emprestimo and data < self.emprestimo.data_emprestimo:
            raise forms.ValidationError('A data de devolução não pode ser anterior ao empréstimo.')
        return data
