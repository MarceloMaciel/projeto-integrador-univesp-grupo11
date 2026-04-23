# BibliotecaPI - Projeto Integrador UNIVESP (Grupo 11)

Sistema web de gerenciamento de biblioteca desenvolvido com Django, incluindo autenticação, catálogo, controle de exemplares e circulação (empréstimos e reservas).

---

## 🌐 Acesso (produção)

Aplicação disponível em:

https://projeto-integrador-univesp-grupo11.onrender.com

---

## 🧠 Visão Geral

O sistema utiliza autenticação padrão do Django e contempla:

* Login e logout
* Troca obrigatória de senha no primeiro acesso
* Cadastro de usuários
* Gestão de catálogo (livros, autores, categorias)
* Controle de exemplares físicos
* Empréstimos, devoluções e reservas

Arquitetura baseada em apps:

* `core`: funcionalidades gerais (home, autenticação, etc.)
* `apps.usuarios`: usuários e permissões
* `apps.catalogo`: livros e metadados
* `apps.acervo`: exemplares
* `apps.circulacao`: empréstimos e reservas

---

## 🛠️ Stack

* Python
* Django 6
* SQLite (desenvolvimento local)
* PostgreSQL (produção)
* Gunicorn
* WhiteNoise
* Bootstrap

---

## ⚙️ Execução Local (desenvolvimento)

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd BibliotecaPI
```

---

### 2. Criar e ativar ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 4. Rodar migrations

```bash
cd BibliotecaPI
python manage.py migrate
```

---

### 5. Criar superusuário

```bash
python manage.py createsuperuser
```

---

### 6. Rodar servidor

```bash
python manage.py runserver
```

Acesse:

```
http://127.0.0.1:8000/
```

---

## 🗄️ Banco de Dados

O projeto detecta automaticamente o ambiente:

* Sem `DATABASE_URL` → usa SQLite (local)
* Com `DATABASE_URL` → usa PostgreSQL

---

## 🚀 Deploy no Render

### ✔ Pré-requisitos

* Conta no Render
* Repositório no GitHub

---

### 1. Criar banco PostgreSQL

No painel do Render:

```
New → PostgreSQL
```

Copie a variável:

```
DATABASE_URL
```

---

### 2. Criar Web Service

```
New → Web Service
```

Conecte ao repositório.

---

### 3. Configurar o serviço

#### Build Command

```bash
pip install -r requirements.txt
```

#### Start Command

```bash
python manage.py migrate && \
python manage.py collectstatic --noinput && \
gunicorn BibliotecaPI.wsgi:application
```

---

### 4. Variáveis de ambiente

No Render:

```
Environment → Add Variable
```

Adicionar:

```
DEBUG=False
SECRET_KEY=sua-chave-segura
ALLOWED_HOSTS=projeto-integrador-univesp-grupo11.onrender.com
DATABASE_URL=postgres://...
```

---

### 5. Deploy

Após salvar, o Render fará o deploy automaticamente.

---

## 🎨 Arquivos Estáticos

* Local: servidos automaticamente pelo Django
* Produção: coletados com `collectstatic` e servidos via WhiteNoise

---

## 🔐 Administração

Painel admin:

```
/admin
```

---

## ⚠️ Problemas comuns

### ❌ DisallowedHost

Verifique `ALLOWED_HOSTS`

---

### ❌ Static não carrega

* Rodar `collectstatic`
* Verificar WhiteNoise

---

### ❌ Gunicorn não encontrado

Verificar `requirements.txt`

---

## 👥 Colaboração

* Código: GitHub
* Infraestrutura: Render (Team)

---

## 📦 Estrutura

```
BibliotecaPI/
├── manage.py
├── BibliotecaPI/
├── core/
├── apps/
├── templates/
└── static/
```

---

## 🧾 Licença

Projeto acadêmico - UNIVESP
