from setuptools import setup, find_packages

setup(
    name='photogal',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Pillow',
        'SQLAlchemy'
    ],
)
