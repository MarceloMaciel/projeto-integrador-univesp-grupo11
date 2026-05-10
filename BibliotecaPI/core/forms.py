from django import forms
from apps.catalogo.models import  Livro

class LivroForm(forms.ModelForm):

    class Meta:
        model = Livro

        fields = [
            'titulo',
            'isbn',
            'autores',
            'editora',
            'categoria',
            'ano_publicacao',
        ]
