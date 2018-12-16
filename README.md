# webscraping_climatempo
Projeto para obter dados do site climatempo em Python, usando biblioteca Selenium e BeautifulSoup

# Requisitos
- Python3
- bibliotecas: selenium, bs4 e pandas
- ter o browser google chrome instalado no seu S.O


## Configurando o pyenv na sua máquina Linux (Opcional)
instalar pyenv: https://github.com/pyenv/pyenv#basic-github-checkout

instalar pyenv-virtualenv: https://github.com/pyenv/pyenv-virtualenv

Obs: caso não use `bash_profile`, troque para `bashrc`

com pyenv instalado configure seu ambiente:
```bash
# Comando para saber se você têm a versão 3.6.4 instalada.
# Se tiver instalado retornará o seguinte: 3.6.4
pyenv versions
    # Caso contrário instale a versão
    pyenv install 3.6.4
    # Setar a versão como global, assim poderá utilizar apenas o comando: python para qualquer execução.
    pyenv global 3.6.4

# comandos para configurar seu ambiente de acordo com a versão requerida
pyenv virtualenv -p python3.6 3.6.4 webscraping_climatempo
# caso não apareça o nome do projeto no caminho do diretório após executar o comando abaixo, 
# feche e abre novamente sua IDE (vscode).
pyenv local webscraping_climatempo

# listar como ficou o seu ambiente (opcional)
ll ~/.pyenv/versions/webscraping_climatempo/bin 
```

## Instalar as dependencias no ambiente local

`pip install -r requirements.txt`

## SETUP.PY

Caso não tenha o diretório: webscraping_climatempo.egg-info
execute o comando abaixo para configurar o projeto:

```bash
# modo de develop: https://setuptools.readthedocs.io/en/latest/setuptools.html#specifying-your-project-s-version
python setup.py develop

```

```bash
# modo de build: https://setuptools.readthedocs.io/en/latest/setuptools.html#specifying-your-project-s-version
python setup.py build
```


## EXECUÇÃO

```bash
# basta executar o comando abaixo
webscraping_climatempo
```
