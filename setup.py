from setuptools import setup, find_packages
import gnb
from pathlib import PurePosixPath

def read(fname):
    '''
    Read the README
    '''
    return open(PurePosixPath(__file__).parent.joinpath(fname)).read()

setup(
    name = 'gnb',
    version = gnb.__version__,
    description = gnb.__description__,
    long_description=read('README.md'),
    classifiers = ['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: GNU Affero General ' +
                   'Public License v3 or later (AGPLv3+)',
                   'Programming Language :: Python :: 3.5',
                   'Topic :: Scientific/Engineering :: Bio-Informatics',
                   'Topic :: Scientific/Engineering :: Medical Science Apps.',
                   'Intended Audience :: Science/Research',
                   "Programming Language :: Python :: 3.7"],
    keywords = ["database merge",
                "GISAID",
                "NCBI",
                "SARS-CoV-2",
                "COVID-19"
                "SRA",
                "BioSample"],
    download_url = gnb.__download_url__,
    author = gnb.__author__,
    author_email = gnb.__author_email__,
    license = gnb.__license__,
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.7",
    include_package_data = True,
    install_requires = ["pandas>=0.25.3",
                        "xlrd>=1.0.0"],
    extras_require={"test": ["pytest", "pytest-cov"],
    },
    package_data={"": ["*.xlsx", "*.xls", "*.json", "*.tsv"]},
    entry_points={"console_scripts": ["gnb = gnb.__main__:main"]},
    project_urls={
        "Bug Reports": "https://github.com/schultzm/gnb/issues",
        "Source": "https://github.com/schultzm/gnb/",
    },
)
