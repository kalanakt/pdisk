from setuptools import setup, find_packages
import codecs
import os


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "package.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.1'
DESCRIPTION = 'An Unofficial Asynchronous Python version of pdisk API wrapper'

# Setting up
setup(
    name="pdisk",
    version=VERSION,
    author="kalanakt",
    license="MIT",
    author_email="kalanakt@uvew.xyz",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    url="https://github.com/kalanakt/pdisk",
    keywords=['python', 'pdisk', 'earn money '],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
