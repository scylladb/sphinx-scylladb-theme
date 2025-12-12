#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    readme = f.read()

setup(
    name="sphinx-scylladb-markdown",
    description="Sphinx extension for ScyllaDB documentation with enhanced Markdown support through MystParser and recommonmark.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="David Garcia",
    author_email="hi@davidgarcia.dev",
    url="https://github.com/scylladb/sphinx-scylladb-theme",
    version="0.1.4",
    install_requires=[
        "sphinx >= 2.1",
        "recommonmark == 0.7.1",
        "sphinx-markdown-tables == 0.0.17",
        "myst-parser >= 2.0.0",
    ],
    packages=["sphinx_scylladb_markdown"],
)
