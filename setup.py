import os
from setuptools import find_packages, setup

this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, 'README.md'), 'r') as fh:
    long_description = fh.read()

setup(
    name='pyimgflip',
    version='0.0.1',
    author='Caleb Bell',
    author_email='caleb@theceebee.com',
    description='An open source Python wrapper for the imgflip RESTful API (https://api.imgflip.com).',
    keywords='imgflip meme API',
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
        'requests',
        'six'
    ],
    python_requires='>=2.7'
)
