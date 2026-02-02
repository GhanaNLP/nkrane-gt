# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="nkrane",
    version="0.2.0",
    author="GhanaNLP",
    author_email="contact@ghananlp.org",
    description="Enhanced Machine Translation with Terminology Control",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GhanaNLP/nkrane",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "nkrane": ["sample_terminology.csv"],
    },
    entry_points={
        "console_scripts": [
            "nkrane=nkrane.cli:main",
        ],
    },
)
