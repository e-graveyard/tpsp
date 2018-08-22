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

    init()

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


def main():
    cptm = CPTM()
    metro = Metro()

    cptm_line_status = []
    for c in cptm.fetch_data():
        cptm_line_status.append([
            c['line'], c['status']
        ])

    metro_line_status = []
    for m in metro.fetch_data():
        metro_line_status.append([
            m['line'], c['status']
        ])

    print(tabulate(cptm_line_status, headers=['Linha', 'Status']))
    print(tabulate(metro_line_status, headers=['Linha', 'Status']))


if __name__ == '__main__':
    main()
