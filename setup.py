from setuptools import setup, find_packages

setup(
    name="apartment-allocator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy>=1.4.0",
    ],
    entry_points={
        'console_scripts': [
            'apartment-allocator=apartment_allocator.cli:main',
        ],
    },
    author="Developer",
    description="Apartment Unit Allocation CLI Application",
)