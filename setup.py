import textwrap
from setuptools import find_packages, setup


with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pyimgflip',
    version='0.0.1',
    author='Caleb Bell',
    author_email='caleb@theceebee.com',
    description=textwrap.dedent('''\
        An unofficial, open source Python and CLI wrapper for the imgflip
        RESTful API (https:\\api.imgflip.com).'''),
    keywords='imgflip meme',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/theceebee/pyimgflip',
    packages=[p for p in find_packages() if p != 'tests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    install_requires=[
        'requests>=2.23',
        'six>=1.14'
    ],
    python_requires='>=2.7'
)
