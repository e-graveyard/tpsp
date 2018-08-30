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


PROGRAM_NAME    = 'tps'
PROGRAM_AUTHOR  = 'Caian R. Ertl'
PROGRAM_VERSION = 'v0.1.0'

COPYRIGHT_INFO  = """
** MIT License **

Copyright (c) 2018 Caian Rais Ertl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class CLI:
    def __init__(self):
        ds = DataSource()
        self.sources = [s for s in ds.all]

        self.parser = ArgumentParser(
            prog=PROGRAM_NAME,
            formatter_class=RawTextHelpFormatter,

            description=textwrap.dedent('''\
                tps: transporte público de São Paulo

                tps (portuguese for "São Paulo public transportation")
                is a tiny command-line tool that tells you the current
                status of CPTM's and Metro lines.
                '''),

            epilog=textwrap.dedent('''\
                examples:
                    $ tps -s cptm
                    # => shows the current state of all CPTM lines

                    $ tps -s metro --json
                    # => shows the current state of all Metro lines and formats
                         the output in JSON

                This is a Free and Open-Source Software (FOSS).
                Licensed under the MIT License.

                Project page: <https://github.com/caianrais/dora>'''))

        # --------------------------------------------------

        self.parser.add_argument(
            'service',
            action='store',
            choices=self.sources,
            default=self.sources[0],
            nargs=1,
            type=str,
            help='the public transportation service')

        self.parser.add_argument(
            '-v', '--version',
            action='version',
            version='{0} ({1})'.format(
                PROGRAM_NAME, PROGRAM_VERSION
            ),
            help='show the program version and exit')

        self.parser.add_argument(
            '-j', '--json',
            action='store_true',
            dest='json',
            help='show the output in JSON format')

        self.parser.add_argument(
            '--copyright',
            action='store_true',
            dest='copyright',
            help='show the copyright information and exit')

    def act(self):
        argp = self.parser.parse_args()

        if argp.copyright:
            print(COPYRIGHT_INFO)

        else:
            pass


class DataSource:
    @property
    def all(self):
        for ds in DataSource.__subclasses__():
            yield ds.__name__.lower()


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
    cli = CLI()
    cli.act()


if __name__ == '__main__':
    main()
