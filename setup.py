from setuptools import setup, find_packages

setup(
    name='photogal',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-GraphQL',
        'Flask-SQLAlchemy',
        'Pillow',
        'SQLAlchemy',
        'graphene_sqlalchemy'
    ],
)
