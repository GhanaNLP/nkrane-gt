# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nkrane-gt",
    version="0.2.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Enhanced Machine Translation with Terminology Control for Google Translate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nkrane",
    packages=find_packages(),
    package_dir={'nkrane_gt': 'nkrane_gt'},
    package_data={
        'nkrane_gt': ['data/*.pkl'],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "googletrans==4.0.0-rc1",
        "spacy>=3.0.0",
        "pandas>=1.0.0",
    ],
    extras_require={
        'dev': [
            'pytest',
            'black',
            'flake8',
        ],
    },
    entry_points={
        'console_scripts': [
            'nkrane-gt=nkrane_gt.cli:main',
        ],
    },
)
