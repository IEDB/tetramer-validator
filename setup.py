import setuptools
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="tetramer_validator",
    version="0.0.1",
    author="IEDB",
    author_email="help@iedb.org",
    description="A small package to validate tetramers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IEDB/tetramer-validator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["openpyxl"],
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "tetramer_validator=tetramer_validator.cli:main",
        ]}
)
