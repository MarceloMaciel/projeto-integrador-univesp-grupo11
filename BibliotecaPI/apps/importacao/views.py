import csv
import io

from django.contrib import messages
from django.shortcuts import redirect, render

from apps.catalogo.models import Autor, Categoria, Editora, Livro
from apps.acervo.models import Exemplar

from .forms import ImportacaoCSVForm


def importar_csv(request):
    if request.method == 'POST':
        form = ImportacaoCSVForm(request.POST, request.FILES)

        if form.is_valid():
            arquivo = request.FILES['arquivo']

            conteudo = arquivo.read().decode('utf-8')

            reader = csv.DictReader(io.StringIO(conteudo))

            for linha in reader:

                autor, _ = Autor.objects.get_or_create(
                    nome=linha['autor']
                )

                categoria, _ = Categoria.objects.get_or_create(
                    nome=linha['categoria']
                )

                editora, _ = Editora.objects.get_or_create(
                    nome=linha['editora']
                )

                livro, created = Livro.objects.get_or_create(
                    isbn=linha['isbn'],
                    defaults={
                        'titulo': linha['titulo'],
                        'editora': editora,
                        'categoria': categoria,
                        'ano_publicacao': linha['ano_publicacao'],
                    }
                )

                livro.autores.add(autor)

                quantidade = int(linha['quantidade'])

                for i in range(quantidade):
                    Exemplar.objects.create(
                        livro=livro,
                        codigo_tombo=f"{livro.id}-{i}"
                    )

            messages.success(request, 'Importação realizada com sucesso.')
            return redirect('importar_csv')

    else:
        form = ImportacaoCSVForm()

    return render(
        request,
        'importacao/importar_csv.html',
        {'form': form}
    )