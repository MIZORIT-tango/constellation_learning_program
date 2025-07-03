from setuptools import setup, find_packages

setup(
    name="constellation_learning_program",
    version="0.1",
    author='MIZORIT-tango',
    author_email='mizmailovartem@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'SQLAlchemy>=2.0.40',
        'PyQt5>=5.15.11',
        'PyQt5-sip>=12.17.0',
    ],
)