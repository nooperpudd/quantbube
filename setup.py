import codecs
import os
import re

from setuptools import setup, find_packages


def find_version(*file_paths):
    """
    Don't pull version by importing package as it will be broken due to as-yet uninstalled
    dependencies, following recommendations at  https://packaging.python.org/single_source_version,
    extract directly from the init file
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *file_paths), 'r') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


install_requires = [item.strip() for item in open('requirements.txt').readlines()]

tests_require = [item.strip() for item in open('requirements-dev.txt').readlines()]

setup(
    name="quantbube",
    version=find_version("quantbube", "__init__.py"),
    author="Winton Wang",
    keywords=["Quantitative Analysis",
              "Trading Bot",
              "Trading Strategy",
              "Time-series Kit",
              "Investment Framework"],
    author_email="winton@quant.vc",
    description="Quantitative Analysis and Trading Strategy Framework",
    long_description=open("README.rst"),
    license="GNU Lesser General Public License v3 or later (LGPLv3+)",
    url="https://github.com/nooperpudd/quantbube",
    packages=find_packages(exclude=["tests", "test.*", "sample"]),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,

    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
