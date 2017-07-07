from distutils.core import setup
setup(
    name='TowelStuff',
    version='0.1',
    author='Arquanum',
    description=' Intelligence gathering freamwork',
    packages=['apis','constants','dbmanagment','feeds'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
)
