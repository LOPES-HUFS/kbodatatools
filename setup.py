import setuptools

NAME = "kbo-data-tool"
DESCRIPTION = "KBO data wrangling & analysis tool"
URL = "https://github.com/LOPES-HUFS/KBO_data_analysis"
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
    packages=setuptools.find_packages(),
    install_requires=REQUIRED,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)