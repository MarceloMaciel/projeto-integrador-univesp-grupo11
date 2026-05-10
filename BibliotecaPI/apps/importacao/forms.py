from django import forms


class ImportacaoCSVForm(forms.Form):
    arquivo = forms.FileField()