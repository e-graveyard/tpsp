#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages
from setuptools import setup
from setuptools import Command


# Metadata
NAME = "tpsp"
DESCRIPTION = "CLI to CPTM and Metro lines status"
URL = "https://github.com/caian-org/tpsp"
EMAIL = "hi@caian.org"
AUTHOR = "Caian R. Ertl"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.1.4"
REQUIRED = [
    "appdirs==1.4.4",
    "beautifulsoup4==4.9.3",
    "bs4==0.0.1",
    "certifi==2020.12.5",
    "chardet==4.0.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
    "colorama==0.4.4",
    "cssselect==1.1.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
    "fake-useragent==0.1.11",
    "idna==2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
    "importlib-metadata==2.1.1; python_version < '3.8'",
    "lxml==4.6.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
    "parse==1.19.0",
    "pyee==8.1.0",
    "pyppeteer==0.2.5; python_full_version >= '3.6.1' and python_full_version < '4.0.0'",
    "pyquery==1.4.3",
    "requests-html==0.10.0",
    "requests==2.25.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
    "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
    "soupsieve==2.1; python_version >= '3.0'",
    "tabulate==0.8.7",
    "tqdm==4.56.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
    "urllib3==1.26.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
    "w3lib==1.22.0",
    "websockets==8.1; python_full_version >= '3.6.1'",
    "zipp==3.4.0; python_version >= '3.6'",
]

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, "docs/README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

about = {}
if not VERSION:
    with open(os.path.join(here, NAME, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

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
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    include_package_data=True,
    license="CC0",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Environment :: Console",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={"console_scripts": ["tpsp = tpsp:main"]},
    # $ setup.py publish support.
    cmdclass={
        "upload": UploadCommand,
    },
)
