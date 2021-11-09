#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages
from setuptools import setup
from setuptools import Command

from tpsp import PROGRAM_NAME
from tpsp import PROGRAM_VERSION
from tpsp import PROGRAM_DESCRIPTION
from tpsp import PROGRAM_URL


# Metadata
REQUIRES_PYTHON = ">=3.6.1"
REQUIRED = [
    "appdirs==1.4.4",
    "beautifulsoup4==4.10.0; python_version >= '3.1'",
    "bs4==0.0.1",
    "certifi==2021.10.8",
    "charset-normalizer==2.0.7; python_version >= '3'",
    "colorama==0.4.4",
    "cssselect==1.1.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
    "fake-useragent==0.1.11",
    "idna==3.3; python_version >= '3'",
    "importlib-metadata==4.8.2; python_version >= '3.6'",
    "lxml==4.6.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
    "parse==1.19.0",
    "pyee==8.2.2",
    "pyppeteer==0.2.6; python_full_version >= '3.6.1' and python_version < '4'",
    "pyquery==1.4.3",
    "requests-html==0.10.0",
    "requests==2.26.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5'",
    "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2'",
    "soupsieve==2.3; python_version >= '3.6'",
    "tabulate==0.8.9",
    "tqdm==4.62.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
    "urllib3==1.26.7; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
    "w3lib==1.22.0",
    "websockets==9.1; python_full_version >= '3.6.1'",
    "zipp==3.6.0; python_version >= '3.6'",
]

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, "docs/README.md"), encoding="utf-8") as f:
        LONG_DESCRIPTION = "\n" + f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = PROGRAM_DESCRIPTION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(text):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(text))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(PROGRAM_VERSION))
        os.system("git push --tags")

        sys.exit()


setup(
    name=PROGRAM_NAME,
    version=PROGRAM_VERSION,
    description=PROGRAM_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Caian R. Ertl",
    author_email="hi@caian.org",
    python_requires=REQUIRES_PYTHON,
    url=PROGRAM_URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    include_package_data=True,
    license="CC0",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={"console_scripts": ["tpsp = tpsp:main"]},
    # $ setup.py publish support.
    cmdclass={
        "upload": UploadCommand,
    },
)
