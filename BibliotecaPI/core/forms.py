from django import forms

from apps.acervo.models import Exemplar
from apps.catalogo.models import Autor, Categoria, Editora, Livro as LivroCatalogo

from .models import LoteCadastro


class LoteForm(forms.ModelForm):
    class Meta:
        model = LoteCadastro
        fields = ['nota_fiscal', 'quantidade']
        widgets = {
            'nota_fiscal': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']
        if quantidade < 1:
            raise forms.ValidationError('Informe ao menos um exemplar para o lote.')
        return quantidade


class LivroForm(forms.Form):
    titulo = forms.CharField(max_length=220, label='Título')
    subtitulo = forms.CharField(max_length=220, required=False, label='Subtítulo')
    isbn = forms.CharField(max_length=17, validators=[LivroCatalogo.isbn_validator], label='ISBN')
    ano_publicacao = forms.IntegerField(min_value=1450, max_value=2100, label='Ano de publicação')
    edicao = forms.CharField(max_length=50, required=False, label='Edição')
    autor = forms.CharField(max_length=180, label='Autor principal')
    editora = forms.CharField(max_length=180, required=False, label='Editora')
    categoria = forms.CharField(max_length=120, required=False, label='Categoria')
    codigo_tombo = forms.CharField(max_length=50, label='Código de patrimônio/tombo')
    codigo_barras_interno = forms.CharField(max_length=50, required=False, label='Código de barras interno')
    localizacao_fisica = forms.CharField(max_length=150, label='Localização física')
    observacoes = forms.CharField(
        required=False,
        label='Observações',
        widget=forms.Textarea(attrs={'rows': 3}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean_codigo_tombo(self):
        codigo_tombo = self.cleaned_data['codigo_tombo'].strip()
        if Exemplar.objects.filter(codigo_tombo__iexact=codigo_tombo).exists():
            raise forms.ValidationError('Já existe um exemplar com este tombo.')
        return codigo_tombo

    def clean_codigo_barras_interno(self):
        codigo_barras = self.cleaned_data.get('codigo_barras_interno', '').strip()
        if codigo_barras and Exemplar.objects.filter(codigo_barras_interno__iexact=codigo_barras).exists():
            raise forms.ValidationError('Já existe um exemplar com este código de barras.')
        return codigo_barras

    def save(self, lote):
        cleaned = self.cleaned_data
        autor = self._get_or_create_by_name(Autor, cleaned['autor'])
        editora = self._get_or_create_by_name(Editora, cleaned['editora']) if cleaned.get('editora') else None
        categoria = self._get_or_create_by_name(Categoria, cleaned['categoria']) if cleaned.get('categoria') else None

        livro, created = LivroCatalogo.objects.get_or_create(
            isbn=cleaned['isbn'],
            defaults={
                'titulo': cleaned['titulo'],
                'subtitulo': cleaned.get('subtitulo', ''),
                'ano_publicacao': cleaned['ano_publicacao'],
                'edicao': cleaned.get('edicao', ''),
                'editora': editora,
            },
        )

        if not created:
            update_fields = []
            for field_name in ('subtitulo', 'edicao'):
                if not getattr(livro, field_name) and cleaned.get(field_name):
                    setattr(livro, field_name, cleaned[field_name])
                    update_fields.append(field_name)
            if livro.editora_id is None and editora:
                livro.editora = editora
                update_fields.append('editora')
            if update_fields:
                livro.save(update_fields=update_fields)

        livro.autores.add(autor)
        if categoria:
            livro.categorias.add(categoria)

        return Exemplar.objects.create(
            livro=livro,
            codigo_tombo=cleaned['codigo_tombo'],
            codigo_barras_interno=cleaned.get('codigo_barras_interno') or None,
            localizacao_fisica=cleaned['localizacao_fisica'],
            observacoes=cleaned.get('observacoes', ''),
            lote_cadastro=lote,
        )

    @staticmethod
    def _get_or_create_by_name(model, name):
        normalized_name = name.strip()
        instance = model.objects.filter(nome__iexact=normalized_name).first()
        if instance:
            return instance
        return model.objects.create(nome=normalized_name)
