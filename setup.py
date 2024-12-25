from setuptools import setup, find_packages

setup(
    name='mktcli',
    version='0.1.0',
    author='yas',
    packages=find_packages(),
    install_requires=['requests', 'click', 'yfinance', 'pandas', 'bs4', 'numpy'],
    entry_points='''[console_scripts]
    mktcli=src.market_cli:mktcli'''
)
