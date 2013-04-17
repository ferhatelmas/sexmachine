from distutils.core import setup

setup(
    name='SexMachine',
    version='0.1.0',
    author='Ferhat Elmas',
    author_email='elmas.ferhat@gmail.com',
    packages=['sexmachine', 'sexmachine.test'],
    url='http://pypi.python.org/pypi/SexMachine/',
    license='LICENSE.txt',
    description='Get the gender from first name.',
    long_description=open('README.rst').read(),
)