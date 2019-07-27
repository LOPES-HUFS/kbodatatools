import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KBO data wrangling & analysis tool",
    version="0.0.1",
    author="Sunsick Choo",
    author_email="~~@~~~",
    description="pKBO data wrangling & analysis tool",
    long_description="KBO data wrangling & analysis tool",
    long_description_content_type="markdown",
    url="https://github.com/LOPES-HUFS/KBO_data_analysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)