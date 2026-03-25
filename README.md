Projeto Integrador Univesp - Grupo 11
Este repositório tem como objetivo guardar o código-fonte do projeto integrador desenvolvido pelo grupo 11 da Univesp.

Instruções para executar a aplicação (Ambiente Windows)
1. Pré-requisitos (Instalação)
Instalar Python:
Execute winget install 9NQ7512CXL7T no terminal, ou baixe a versão mais atual no site oficial: python.org/downloads.

Para checar a instalação, rode: python --version ou py --version.

Instalar Git:
Execute winget install --id Git.Git -e --source winget no terminal, ou baixe a versão mais atual no site oficial: git-scm.com.

2. Configuração do Ambiente
Clonar o repositório:
Escolha um local no seu computador e execute:

PowerShell
git clone https://github.com/MarceloMaciel/projeto-integrador-univesp-grupo11.git
cd projeto-integrador-univesp-grupo11
Criar ambiente virtual:

PowerShell
python -m venv venv
Ativar o ambiente virtual:

PowerShell
venv\Scripts\activate
Nota: Se encontrar erro de permissão no PowerShell, execute:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Instalar dependências:

PowerShell
pip install -r requirements.txt
3. Execução do Projeto
Para rodar os comandos do Django, é necessário entrar na subpasta onde o arquivo manage.py está localizado:

Entrar na pasta do sistema:

PowerShell
cd BibliotecaPI
Aplicar migrations (Configurar Banco de Dados):

PowerShell
python manage.py migrate
Rodar o servidor:

PowerShell
python manage.py runserver
O sistema estará disponível no seu navegador no endereço: http://127.0.0.1:8000/