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
    from colorama import init
    from colorama import Fore
    from colorama import Style

    init(autoreset=True)

except ImportError as e:
    print('SPT: impossible to import 3rd-party libraries.\n'
          'Latest traceback: {0}' . format(e.args[0]))

    sys.exit(1)


class CLI:
    pass


class DataSource:
    @property
    def all(self):
        for ds in DataSource.__subclasses__():
            yield ds


class CPTM(DataSource):
    def __init__(self):
        self.url = 'http://cptm.sp.gov.br/'
        self.session = HTMLSession()
        self.html_line_refs = ['rubi', 'diamante', 'esmeralda', 'turquesa',
                               'coral', 'safira', 'jade']

    def fetch_data(self):
        res = self.session.get(self.url)

        for ref in self.html_line_refs:
            data = res.html.find('.{0}'.format(ref), first=True)
            yield {
                'line': ref.capitalize(),
                'status': data.text.replace(ref.upper(), '')
            }


class Metro(DataSource):
    def __init__(self):
        self.url = 'http://www.metro.sp.gov.br/sistemas/direto-do-metro-via4/index.aspx'
        self.session = HTMLSession()
        self.html_line_refs = ['l1', 'l2', 'l3', 'l4', 'l5', 'l15']

    def fetch_data(self):
        res = self.session.get(self.url)

        for ref in self.html_line_refs:
            data = res.html.find('.{0}'.format(ref), first=True)

            _, data = tuple(data.text.split('-'))
            data = data.split(' ')
            yield {
                'line': data[0],
                'status': ' '.join(map(str, data[1:]))
            }


def beautify(data):
    def header(cols):
        H = []
        for c in cols:
            H.append('{}{}{}'.format(Style.BRIGHT, c, Style.RESET_ALL))

        return H

    beautiful_data = []
    for d in data:
        line = d['line']
        stat = d['status']

        formatting = Fore.WHITE
        if stat.lower() == 'operação normal':
            formatting = Fore.GREEN

        elif stat == 'velocidade reduzida':
            formatting = Fore.YELLOW

        elif stat == 'operação encerrada':
            formatting = Style.DIM

        beautiful_data.append([
            '{}'.format(line),
            '{}{}{}'.format(formatting, stat, Style.RESET_ALL)
        ])

    return tabulate(beautiful_data, headers=header(['Linha', 'Status']))


def main():
    cptm = CPTM()
    metro = Metro()

    print(beautify(cptm.fetch_data()) + '\n')
    print(beautify(metro.fetch_data()))


if __name__ == '__main__':
    main()
