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
        self.sources = [s for s in Service.all()]

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
        return self.parser.parse_args()


class Service:
    @staticmethod
    def all():
        for ds in Service.__subclasses__():
            yield ds.__name__.lower()


class CPTM(Service):
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


class Metro(Service):
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


class Output:
    def __init__(self, data):
        self.data = data

    @property
    def table(self):
        def header(cols):
            for c in cols:
                yield '{}{}{}'.format(Style.BRIGHT, c, Style.RESET_ALL)

        def line_status(status):
            color = Fore.WHITE
            if 'normal' in status:
                color = Fore.GREEN

            elif 'reduzida' in status:
                color = Fore.YELLOW

            elif 'encerrada' in status:
                color = Style.DIM

            return '{}{}{}'.format(color, status, Style.RESET_ALL)

        def beautify():
            for d in self.data:
                yield [
                    d['line'], line_status(d['status'].lower())
                ]

        cols = ['Linha', 'Status']
        data = [d for d in beautify()]
        head = [h for h in header(cols)]

        return tabulate(data, headers=head)

    @property
    def json(self):
        pass


def main():
    cli = CLI()
    cli.act()


if __name__ == '__main__':
    main()
