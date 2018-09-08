# TPS: Transporte Público de São Paulo

`tps` (acrônimo de "Transporte Público de São Paulo") é uma pequena aplicação
escrita em Python cujo objetivo é exibir o estado atual das linhas da [CPTM] e
[Metro].

**AVISO: Este projeto não possui relações com o Estado de São Paulo, a CPTM, o
Metro ou qualquer outro órgão governamental.**

[CPTM]: https://www.cptm.sp.gov.br/
[Metro]: http://www.metro.sp.gov.br/sistemas/direto-do-metro-via4/index.aspx


## Sumário

- [Requerimentos](#requerimentos)
- [Dependências](#dependencias)
- [Funcionamento](#funcionamento)
- [Uso](#uso)


## Requerimentos

- Python (3.4 ou superior).


## Dependências

- [`requests-html`](https://github.com/kennethreitz/requests-html)
- [`colorama`](https://github.com/tartley/colorama)
- [`tabulate`](https://bitbucket.org/astanin/python-tabulate)

## Funcionamento

Não há, até a data de publicação desta aplicação, uma API pública para os
serviços de trem e metrô do Estado de São Paulo. Os dados utilizados por esta
aplicação são obtidos mediante [web scraping] das páginas online dos serviços.

O fluxo é relativamente simples:
1. O parser recebe os argumentos e flags da linha de comando;
1. Uma requisição `GET` é enviada à página do serviço a ser consultado;
1. O conteúdo `HTML` é analisado, quebrado a partir da estrutura e filtrado;
1. os trechos de interesse do conteúdo (as `divs` / `.class` que guardam os
   nomes das linhas e seus respectivo status) são retidos;
1. Os dados das linhas são formatados e impressos na tela.

Cada resultado é filtrado e manipulado a partir das especificidades da construção
da página web do serviço. Apesar de contraproducente, uma vez que mudanças na
contrução das páginas podem (e vão) quebrar a funcionalidade, este foi o melhor
approach encontrado.

[web scraping]: https://en.wikipedia.org/wiki/Web_scraping


## Instalação

```sh
# clone o repositório
$ git clone https://github.com/caianrais/tps && cd tps

# instale as dependências
$ (sudo) pip3 install requests-html colorama tabulate

# mova o script para algum diretório mapeado na variável de ambiente $PATH
$ mv src/tps.py ~/bin
```

*Em breve: `tps` no PyPI*


## Uso

```
positional arguments:
  {cptm,metro}   the public transportation service

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show the program version and exit
  -j, --json     show the output in JSON format
  --copyright    show the copyright information and exit

examples:
    $ tps cptm
    # => shows the current state of all CPTM lines

    $ tps metro --json
    # => shows the current state of all Metro lines and formats
         the output in JSON
```
