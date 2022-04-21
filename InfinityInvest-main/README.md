### Instalação Python

Link para download do Python3 32bits: [link](https://www.python.org/ftp/python/3.6.5/python-3.6.5.exe)

Após baixar o instalador do Python execute-o e selecione a opção "Customize installation" 

![Python1](https://github.com/MatheusGalhani/InfinityInvest/blob/main/media/Python1.jpg)

Marque todas as opções e clique em "Next"

![Python2](https://github.com/MatheusGalhani/InfinityInvest/blob/main/media/Python2.jpg)

Alterer o caminho de instalação para "C:\Python36" e clique em "Install"

![Python3](https://github.com/MatheusGalhani/InfinityInvest/blob/main/media/Python3.jpg)


### Configurando Python3 - Variáveis de ambientes

Para que possamos utilizar o Python de forma mais simples, devemos adicionar 2 pastas a variavel de ambiente "PATH". Para isso aperte "Windows + Pause Break".

Selecione a opção "Advanced system settings"

![Variaveis1](https://github.com/MatheusGalhani/InfinityInvest/blob/main/media/variaveis1.jpg)

Selecione a opção "Environment variable"

![Variaveis2](https://github.com/MatheusGalhani/InfinityInvest/blob/main/media/variaveis2.jpg)

Selecione "PATH"

![Variaveis3](https://github.com/MatheusGalhani/InfinityInvest/blob/main/media/variaveis3.jpg)

Insira as seguintes pastas "C:\Python36" e "C:\Python36\Scripts"

![Variaveis4](https://github.com/MatheusGalhani/InfinityInvest/blob/main/media/variaveis4.jpg)

### Executando o projeto

Para puxarmos as dependencias do projeto devemos conectar via cmd no diretório que o projeto está presente e executar o comando abaixo
````
pip install -r requirements.txt
````

Após termos as bibliotecas baixadas, devemos startar o projeto com o comando:
````
python manage.py runserver
````

### Super Usuário
```
Usuário: infinityinvest@infinityinvest.com
Senha: DevInfinityPass
```

### Links de apoio
[Django Girl](https://tutorial.djangogirls.org/pt/django_start_project/)

[Medium Api Parte 1](https://medium.com/@apogiatzis/create-a-restful-api-with-users-and-jwt-authentication-using-django-1-11-drf-part-1-288268602bb7)

[Medium Api Parte 2](https://medium.com/@apogiatzis/create-a-restful-api-with-users-and-jwt-authentication-using-django-1-11-drf-part-2-eb6fdcf71f45)