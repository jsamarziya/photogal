import os
from glob import glob

from setuptools import setup, find_packages

setup(
    name='photogal',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-GraphQL',
        'Flask-SQLAlchemy',
        'Graphene-SQLAlchemy',
        'Pillow',
        'SQLAlchemy',
        'StringLike'
    ],
)
