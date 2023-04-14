import os

from setuptools import setup


setup(
    name="traffix", 
    version = "0.1.12",
    description = "A package for macroscopic transportation assignment.",
    package_dir = {"":"traffix"},
    author = "Aulia Rahman",
    author_email = "rahmancs02@gmail.com",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    url="https://github.com/Ultios/traffix",
    include_package_data=True,
    classifiers  = [
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        "osmnx >=1.3.0",
        "pandas >=1.5",
        "geopandas>=0.12",
        "matplotlib>=3.5",
        "networkx>=2.8",
        "numpy>=1.23",
        "pandas>=1.5",
        "pyproj>=3.4",
        "requests>=2.28",
        "Shapely>=2.0"
    ],
    
    keywords = ["Traffic Assignment", "Transportation Planning", "Macroscopic Transportation Planning"],
)
