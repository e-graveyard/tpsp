[![Build Status][travis-shield]][travis-url] [![Code Quality][lgtm-shield]][lgtm-url] [![GitHub tag][tag-shield]][tag-url]

[travis-shield]: https://img.shields.io/travis/caian-org/tpsp.svg?logo=travis-ci&logoColor=FFF&style=flat-square
[travis-url]: https://travis-ci.org/caian-org/tpsp

[lgtm-shield]: https://img.shields.io/lgtm/grade/python/g/caian-org/tpsp.svg?logo=lgtm&style=flat-square
[lgtm-url]: https://lgtm.com/projects/g/caian-org/tpsp/context:python

[tag-shield]: https://img.shields.io/github/tag/caian-org/tpsp.svg?logo=git&logoColor=FFF&style=flat-square
[tag-url]: https://github.com/caian-org/tpsp/releases

# TPSP: Transporte Público de São Paulo

`tpsp` (acrônimo para "Transporte Público de São Paulo") é uma pequena aplicação
escrita em Python cujo objetivo é exibir o estado atual das linhas da [CPTM] e
[Metro].

<p align="center">
  <img src="docs/tpsp.gif">
</p>

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

- Python (3.6.1 ou superior).


## Dependências

- [`requests-html`](https://github.com/kennethreitz/requests-html)
- [`colorama`](https://github.com/tartley/colorama)
- [`tabulate`](https://bitbucket.org/astanin/python-tabulate)

## Funcionamento

Não há, até a data de publicação desta aplicação, uma API pública para os
serviços de trem e metrô do Estado de São Paulo. Os dados utilizados por esta
aplicação são obtidos mediante [web scraping] das páginas online dos serviços.

**O fluxo é relativamente simples:**

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
$ pip3 install tpsp
```


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
    $ tpsp cptm
    # => shows the current state of all CPTM lines

    $ tpsp metro --json
    # => shows the current state of all Metro lines and formats
         the output in JSON
```

## Licença

[![Kopimi Logo][kopimi-logo]][kopimi-url]

Na medida do possível sob a lei, [Caian Rais Ertl][me] renunciou a __todos os
direitos autorais e direitos relacionados ou adjacentes a este trabalho__. No
espírito da _liberdade de informação_, encorajo você a forkar, modificar,
alterar, compartilhar ou fazer o que quiser com este projeto! `^ C ^ V`

[![License][cc-shield]][cc-url]

[me]: https://github.com/caiertl
[cc-shield]: https://forthebadge.com/images/badges/cc-0.svg
[cc-url]: http://creativecommons.org/publicdomain/zero/1.0

[kopimi-logo]: https://gist.githubusercontent.com/xero/cbcd5c38b695004c848b73e5c1c0c779/raw/6b32899b0af238b17383d7a878a69a076139e72d/kopimi-sm.png
[kopimi-url]: https://kopimi.com
