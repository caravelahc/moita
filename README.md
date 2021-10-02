# moita

Introdução
==========
O **MOITA** é um servidor de documentos desenvolvido para aprimorar o sistema
[**CAPIM**](https://github.com/caravelahc/capim), que por sua vez foi feito
para substituir o **GRAMA**, cujos objetivos são ajudar os alunos a organizar os
seus horários de aula com um cronograma intuitivo e simplificado que permite
combinar matérias de diversas formas, de forma interativa.

Você pode ler a história e a motivação do CAPIM no repositório indicado pelo
link acima.

Deploy
======
É possível utilizar o servidor MOITA de duas formas:

Flask (não recomendado)
-----------------------------------
Como o MOITA é feito utilizando Flask, é possível utilizar o servidor built-in,
embora isso não seja recomendado pois este servidor não é feito para ambientes
de produção, apenas para testes e desenvolvimento:

```sh
python moita.py
```

uWSGI + Nginx
-------------
O Flask segue a [PEP-333](https://www.python.org/dev/peps/pep-0333/), ou seja,
é possível usar o [uWSGI](https://uwsgi-docs.readthedocs.org/en/latest/) para
subir um servidor. É simples:

```sh
uwsgi -w moita:app -s :5000
```
Ou, de forma mais explícita:
```sh
uwsgi --wsgi moita:app --uwsgi-socket :5000
```
Você pode utilizar uma porta diferente ou até mesmo um UNIX socket. Leia a
[documentação](http://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html)
do uWSGI para maiores informações.

No Nginx, configure seu server da seguinte forma:
```
location / {
    try_files $uri @app;
}

location @app {
    include uwsgi_params;
    uwsgi_pass 127.0.0.1:5000;
}
```
Recarregue o Nginx e tudo deve funcionar :)
