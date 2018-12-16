'''
      configure the webscraping_climatempo app to be installed
'''
from webscraping_climatempo import VERSION
from setuptools import setup, find_packages, os

setup(
    name='webscraping_climatempo',
    version=VERSION,
    description='Project to get climatempo site data',
    url='',
    author='Ericles Henrique',
    author_email='ericles.system@gmail.com',
    license='Public',
    install_requires=[
        'selenium',
        'beautifulsoup4',
        'cython',
        'pandas'
    ],
    packages=find_packages(),
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'webscraping_climatempo=webscraping_climatempo.app:main',
        ],
    },
    include_package_data = True
)
