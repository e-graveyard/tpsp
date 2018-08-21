#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard libraries. Should not fail.
import sys
import textwrap
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter

# Required 3rd-party libraries.
try:
    from requests_html import HTMLSession
    from tabulate import tabulate

except ImportError as e:
    print('SPT: impossible to import 3rd-party libraries.\n'
          'Latest traceback: {0}' . format(e.args[0]))

    sys.exit(1)


class CLI:
    pass


def main():
    session = HTMLSession()
    cptm_url = 'http://cptm.sp.gov.br/'
    metro_url = 'http://www.metro.sp.gov.br/sistemas/direto-do-metro-via4/index.aspx'

    cptm_res = session.get(cptm_url)
    metro_res = session.get(metro_url)

    cptm_res = cptm_res.html.find('#atendimento_consumidor')[0].text.split('\n')
    metro_res = metro_res.html.find('#diretoMetro')[0].text.split('\n')

    cptm_res.pop()
    cptm_res.pop(0)

    metro_res.pop()
    metro_res.pop(0)
    metro_res.pop(3)
    metro_res.pop(4)

    cptm = []
    for c in cptm_res:
        cptm.append(c.split('Operação '))

    print('\n{0}\n{1}\n'.format(
        '===== CPTM =====',
        tabulate(cptm, headers=['Linha', 'Status'])
    ))

    metro = []
    for m in metro_res:
        metro.append(m.split(' Operação '))

    print('\n{0}\n{1}\n'.format(
        '===== METRO =====',
        tabulate(cptm, headers=['Linha', 'Status'])
    ))


if __name__ == '__main__':
    main()
