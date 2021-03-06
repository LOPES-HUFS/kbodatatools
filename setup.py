#!/usr/bin/env python

import setuptools

NAME = "kbodatatools"
DESCRIPTION = "KBO data wrangling & analysis tools"
URL = "https://github.com/LOPES-HUFS/kbodatatools"
EMAIL = "sunsick_choo@naver.com"
AUTHOR = "Sunsick Choo"
VERSION = "0.0.1"
REQUIRED = [
    "pandas", "requests_html", "bs4", "tables", "datetime"
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    python_requires=">=3.6.0",
    packages = ['kbodatatools'],
    package_data={'kbodatatools': ['data/*']},
    package_dir={'kbodatatools': 'kbodatatools'},
    install_requires=REQUIRED,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)