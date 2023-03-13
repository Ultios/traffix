import os

from setuptools import setup

######################################################################################################
################ You May Remove All the Comments Once You Finish Modifying the Script ################
######################################################################################################

setup(
    name="TraffiX", 
    version = "0.1.0-alpha",
    description = "A package for macroscopic transportation assignment.",
    package_dir = {"":"TraffiX"},
    author = "Aulia Rahman",
    author_email = "rahmancs02@gmail.com",
    long_description = open("README.md").read() + "\n\n" + open("CHANGELOG.md").read(),
    long_description_content_type = "text/markdown",
    url="https://github.com/Ultios/StraPy",
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
        "osmnx ~= 1.3.0",
        "pandas ~= 1.2.4",
    ],
    keywords = ["Traffic Assignment", "Transportation Planning", "Macroscopic Transportation Planning"],
)
