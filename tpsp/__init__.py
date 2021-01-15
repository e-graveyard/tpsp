# pylint: disable=too-few-public-methods

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

except ImportError as err:
    print(
        'TPSP: impossible to import 3rd-party libraries.\n'
        'Latest traceback: {0}'.format(err.args[0])
    )

    sys.exit(1)


PROGRAM_NAME = 'tpsp'
PROGRAM_AUTHOR = 'Caian R. Ertl'
PROGRAM_VERSION = 'v0.1.5'

COPYRIGHT_INFO = """
The person who associated a work with this deed has dedicated the work to the
public domain by waiving all of his or her rights to the work worldwide under
copyright law, including all related and neighboring rights, to the extent
allowed by law.

You can copy, modify, distribute and perform the work, even for commercial
purposes, all without asking permission.

AFFIRMER OFFERS THE WORK AS-IS AND MAKES NO REPRESENTATIONS OR WARRANTIES OF
ANY KIND CONCERNING THE WORK, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,
INCLUDING WITHOUT LIMITATION WARRANTIES OF TITLE, MERCHANTABILITY, FITNESS FOR
A PARTICULAR PURPOSE, NON INFRINGEMENT, OR THE ABSENCE OF LATENT OR OTHER
DEFECTS, ACCURACY, OR THE PRESENT OR ABSENCE OF ERRORS, WHETHER OR NOT
DISCOVERABLE, ALL TO THE GREATEST EXTENT PERMISSIBLE UNDER APPLICABLE LAW.

For more information, please see
<http://creativecommons.org/publicdomain/zero/1.0/>
"""


class CLI:
    def __init__(self):
        self.sources = list(Service.all())

        self.parser = ArgumentParser(
            prog=PROGRAM_NAME,
            formatter_class=RawTextHelpFormatter,
            description=textwrap.dedent(
                '''\
                tpsp: transporte público de São Paulo

                tpsp (portuguese for "São Paulo public transportation")
                is a tiny command-line tool that tells you the current
                status of CPTM's and Metro lines.
                '''
            ),
            epilog=textwrap.dedent(
                '''\
                examples:
                    $ tpsp cptm
                    # => shows the current state of all CPTM lines

                    $ tpsp metro --json
                    # => shows the current state of all Metro lines and formats
                         the output in JSON

                This is a Free and Open-Source Software (FOSS).
                Project page: <https://github.com/caian-org/tpsp>'''
            ),
        )

        # --------------------------------------------------

        self.parser.add_argument(
            'service',
            action='store',
            choices=self.sources,
            nargs=1,
            type=str,
            help='the public transportation service',
        )

        self.parser.add_argument(
            '-v',
            '--version',
            action='version',
            version='{0} ({1})'.format(PROGRAM_NAME, PROGRAM_VERSION),
            help='show the program version and exit',
        )

        self.parser.add_argument(
            '-j',
            '--json',
            action='store_true',
            dest='json',
            help='show the output in JSON format',
        )

        self.parser.add_argument(
            '--copyright',
            action=Copyright,
            nargs=0,
            help='show the copyright information and exit',
        )

    def act(self):
        return self.parser.parse_args()


class Copyright(Action):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

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
        self.url = 'https://www.cptm.sp.gov.br/Pages/Home.aspx'
        self.session = HTMLSession()

    def fetch_data(self):
        refs = ['rubi', 'diamante', 'esmeralda', 'turquesa', 'coral', 'safira', 'jade']
        res = self.session.get(self.url)

        for ref in refs:
            data = res.html.find('.{0}'.format(ref), first=True)
            yield {
                'line': ref.capitalize(),
                'status': data.text.replace(ref.upper(), ''),
            }


class METRO(Service):
    def __init__(self):
        self.url = 'http://www.metro.sp.gov.br/Sistemas/direto-do-metro-via4/diretodoMetroHome.aspx'
        self.session = HTMLSession()

    def fetch_data(self):
        res = self.session.get(self.url)

        names = res.html.find('.{0}'.format('nomeDaLinha'))
        stati = res.html.find('.{0}'.format('statusDaLinha'))

        for idx, name in enumerate(names):
            line = name.text.split('-')[1]
            status = stati[idx].text

            yield {'line': line.strip(), 'status': status}


class Output:
    def __init__(self, data):
        self.data = data

    @property
    def table(self):
        def header(cols):
            for col in cols:
                yield '{}{}{}'.format(Style.BRIGHT, col, Style.RESET_ALL)

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
            for data in self.data:
                yield [data['line'], line_status(data['status'].lower())]

        cols = ['Linha', 'Status']
        return tabulate(list(beautify()), headers=list(header(cols)))

    @property
    def json(self):
        return json.dumps(
            {'code': 200, 'data': list(self.data), 'message': 'success'},
            ensure_ascii=False,
            sort_keys=True,
            indent=4,
        )


def main():
    cli = CLI()
    args = cli.act()

    service = getattr(sys.modules[__name__], args.service[0].upper())
    data = service().fetch_data()
    outp = Output(data)

    print('\n{}'.format(outp.json if args.json else outp.table))
