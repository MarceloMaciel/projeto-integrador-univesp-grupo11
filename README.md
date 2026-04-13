# BibliotecaPI - Projeto Integrador Univesp Grupo 11

Sistema web de gerenciamento de biblioteca desenvolvido em Django, com autenticação, catálogo bibliográfico, controle de exemplares, circulação de empréstimos e reservas, e preparação para PostgreSQL no Aiven.

## Visão Geral

A aplicação usa a autenticação padrão do Django e mantém o fluxo acadêmico original de login, logout, troca obrigatória de senha no primeiro acesso, cadastro de usuários e entrada de acervo por lote de nota fiscal.

A modelagem foi organizada em apps:

- `core`: home, troca de senha, lote de entrada e modelos legados mantidos por compatibilidade.
- `apps.usuarios`: cadastro de usuários, grupos e permissões.
- `apps.catalogo`: autores, editoras, categorias e livros/obras.
- `apps.acervo`: exemplares físicos vinculados aos livros.
- `apps.circulacao`: empréstimos, devoluções, reservas, multas e auditoria.

## Stack

- Python
- Django 6.0.3
- Django Templates
- Bootstrap 5.3.3
- SQLite para desenvolvimento local simples
- PostgreSQL via `psycopg` para ambientes com Aiven

## Rotas Principais

- `/`: painel inicial com indicadores do acervo.
- `/login/` e `/logout/`: autenticação.
- `/trocar-senha/`: troca obrigatória da senha inicial.
- `/usuarios/cadastrar/`: cadastro de usuários.
- `/catalogo/`: consulta do catálogo, com filtros por título, autor, ISBN, categoria e disponibilidade.
- `/catalogo/livros/novo/`: cadastro de obras.
- `/acervo/exemplares/`: gestão de exemplares físicos.
- `/circulacao/emprestimos/`: empréstimos, renovações e devoluções.
- `/circulacao/reservas/`: reservas.
- `/iniciar-lote/` e `/cadastrar-livro/`: entrada de exemplares por lote de nota fiscal.

## Permissões

- `ADMIN` e `BIBLIOTECARIO`: podem cadastrar usuários, obras, autores, editoras, categorias, exemplares, lotes, empréstimos e devoluções.
- `LEITOR`: pode consultar o catálogo e criar/acompanhar as próprias reservas.
- Superusuários do Django são tratados como `ADMIN` pelo sistema.

## Configuração Local

Crie e ative o ambiente virtual:

```powershell
python -m venv venv
venv\Scripts\activate
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Copie o arquivo de ambiente:

```powershell
Copy-Item .env.example .env
```

O arquivo `.env` é local e fica fora do versionamento. Use `.env.example` como modelo.

Por padrão, o `.env.example` usa SQLite:

```env
DEBUG=True
DB_ENGINE=sqlite3
DB_NAME=db.sqlite3
```

Entre na pasta do projeto Django:

```powershell
cd BibliotecaPI
```

Execute as migrations:

```powershell
python manage.py migrate
```

Crie um superusuário:

```powershell
python manage.py createsuperuser
```

Rode o servidor local:

```powershell
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

## Variáveis de Ambiente

O projeto lê `.env` na raiz do repositório e também aceita `.env` ao lado de `manage.py`.

Principais variáveis:

```env
SECRET_KEY=django-insecure-troque-esta-chave
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_ENGINE=sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=5432
DB_SSLMODE=require
DB_SSLROOTCERT=
```

## PostgreSQL no Aiven

Para usar PostgreSQL no Aiven, ajuste o `.env` com os dados do serviço:

```env
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,127.0.0.1
DB_ENGINE=postgresql
DB_NAME=nome_do_banco
DB_USER=usuario_aiven
DB_PASSWORD=senha_aiven
DB_HOST=host-do-servico.aivencloud.com
DB_PORT=12345
DB_SSLMODE=require
DB_SSLROOTCERT=
```

Em Aiven, `sslmode=require` costuma ser suficiente para criptografar a conexão. Se a política do ambiente exigir validação do certificado, use `DB_SSLMODE=verify-ca` ou `DB_SSLMODE=verify-full` e informe o caminho do certificado CA em `DB_SSLROOTCERT`.

Depois de apontar para o PostgreSQL, rode:

```powershell
cd BibliotecaPI
python manage.py migrate
python manage.py createsuperuser
```

## Testes

Execute:

```powershell
cd BibliotecaPI
python manage.py test
```

Os testes cobrem login/redirecionamento, troca obrigatória de senha, permissões, cadastro de livro, busca e paginação do acervo, renderização dos formulários, cadastro por lote, empréstimo/devolução com mudança de status do exemplar e validação da data de devolução.

## Administração

O admin do Django está disponível em:

```text
http://127.0.0.1:8000/admin/
```

Os grupos padrão `ADMIN`, `BIBLIOTECARIO` e `LEITOR` são criados automaticamente após as migrations. Usuários com perfil de administrador ou bibliotecário podem cadastrar usuários, obras, exemplares e registrar circulação. O admin usa filtros, buscas, paginação, campos de autocomplete e títulos customizados para facilitar demonstração e operação.

## Interface

A interface usa templates Django em `BibliotecaPI/templates`, Bootstrap 5.3.3 via CDN e ajustes simples em `BibliotecaPI/static/css/app.css`. O `base.html` centraliza navegação, mensagens, bloco de cabeçalho de página e rodapé. Os formulários compartilham o partial `templates/partials/form_fields.html`, e os templates antigos dentro de `core/templates/core` foram removidos para evitar duplicação e rotas legadas.
