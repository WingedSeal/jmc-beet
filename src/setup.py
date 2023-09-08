"""Setup file for pypi"""
from pathlib import Path
from setuptools import setup, find_packages


VERSION = "v0.0.1-alpha.4"

DESCRIPTION = "A Beet plugin that act as an adapter for JMC"
version = VERSION.replace("-alpha.", "a").replace("-beta.", "b")[1:]
setup(
    name="jmc-beet",
    version=version,
    author="WingedSeal",
    author_email="firm09719@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="""
# jmc-beet
A plugin for integrating JMC into Beet
""",
    packages=find_packages(),
    install_requires=[
        "jmcfunction",
        "beet"
    ],
    keywords=[
        "python",
        "minecraft",
        "mcfunction",
        "datapack",
        "compiler",
        "beet"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.10",
    project_urls={
        "Documentation": "https://jmc.wingedseal.com/",
        "Repository": "https://github.com/WingedSeal/jmc-beet",
    },
    license="MIT License"
)
