# projeto-integrador-univesp-grupo11
Este repositório tem como objetivo guardar o código fonte do projeto integrador desenvolvido pelo grupo 11 da univesp.

# Instruções para executar a aplicação (ambiente Windows)
1. Instalar Python
    Executar "winget install 9NQ7512CXL7T" no terminal, ou baixar e instalar na versão mais atual a partir do site oficial: https://www.python.org/downloads/
    Para checar se o python foi devidamente instalado, rode o comando "python --version" ou "py --version"'.
2. Instalar Git
    Executar "winget install --id Git.Git -e --source winget" no terminal, ou baixar e instalar na versão mais atual a partir do site oficial: https://git-scm.com/
3. Clonar o repositório
    Escolher um local no seu computador e clonar o repositório com o comando: "git clone https://github.com/MarceloMaciel/projeto-integrador-univesp-grupo11.git"
4. Criar ambiente virtual (dentro da pasta do projeto):
   python -m venv venv
5. Ativar o ambiente:
   venv\Scripts\activate

Se enfrentar erro ao tentar ativar o ambiente, execute o comando "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" para permitir a utilização do powershell.

6. Instalar dependências:
   pip install -r requirements.txt

7. Aplicar migrations:
   python manage.py migrate

8. Rodar o projeto:
   python manage.py runserver

