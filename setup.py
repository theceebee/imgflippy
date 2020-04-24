import setuptools
import textwrap


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyimgflip-theceebee',
    version='0.0.1',
    author='Caleb Bell',
    author_email='caleb@theceebee.com',
    description=textwrap.dedent('''\
        An unofficial, open source Python and CLI wrapper for the imgflip
        RESTful API (https:\\api.imgflip.com).'''),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages='setuptools.find_packages()'
)

install_requires = [
    'requests>=2.23',
]
