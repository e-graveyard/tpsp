#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard libraries. Should not fail.
import sys
import json
import textwrap

from argparse import Action
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
    print('TPS: impossible to import 3rd-party libraries.\n'
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
                    $ tps cptm
                    # => shows the current state of all CPTM lines

                    $ tps metro --json
                    # => shows the current state of all Metro lines and formats
                         the output in JSON

                This is a Free and Open-Source Software (FOSS).
                Licensed under the MIT License.

                Project page: <https://github.com/caianrais/tps>'''))

        # --------------------------------------------------

        self.parser.add_argument(
            'service',
            action='store',
            choices=self.sources,
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
            action=Copyright,
            nargs=0,
            help='show the copyright information and exit')

    def act(self):
        return self.parser.parse_args()


class Copyright(Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(Copyright, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print(COPYRIGHT_INFO)
        sys.exit(0)


class Service:
    @staticmethod
    def all():
        for ds in Service.__subclasses__():
            yield ds.__name__.lower()


class CPTM(Service):
    def __init__(self):
        self.url = 'http://cptm.sp.gov.br/'
        self.session = HTMLSession()

    def fetch_data(self):
        refs = ['rubi', 'diamante', 'esmeralda', 'turquesa', 'coral', 'safira', 'jade']
        res = self.session.get(self.url)

        for ref in refs:
            data = res.html.find('.{0}'.format(ref), first=True)
            yield {
                'line': ref.capitalize(),
                'status': data.text.replace(ref.upper(), '')
            }


class METRO(Service):
    def __init__(self):
        self.url = 'http://www.metro.sp.gov.br/Sistemas/direto-do-metro-via4/diretodoMetroHome.aspx'
        self.session = HTMLSession()

    def fetch_data(self):
        res = self.session.get(self.url)

        names = res.html.find('.{0}'.format('nomeDaLinha'))
        stati = res.html.find('.{0}'.format('statusDaLinha'))

        for i in range(len(names)):
            name = names[i].text
            name = name.split('-')[1]
            name = name.strip()

            status = stati[i].text

            yield {
                'line': name,
                'status': status
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

            elif 'paralisada' in status:
                color = Fore.RED

            elif 'encerrada' in status:
                color = Style.DIM

            return '{}{}{}'.format(color, status.title(), Style.RESET_ALL)

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
        return json.dumps(
            {
                'code': 200,
                'data': [d for d in self.data],
                'message': 'success'
            },
            ensure_ascii=False,
            sort_keys=True,
            indent=4
        )


def fetch(service):
    service = getattr(sys.modules[__name__], service[0].upper())
    return service().fetch_data()


def main():
    cli = CLI()
    args = cli.act()

    data = fetch(args.service)
    outp = Output(data)

    print('\n{}'.format(
        outp.json if args.json else outp.table
    ))


if __name__ == '__main__':
    main()
