#!/bin/bash

cd .. && poetry run sphinx-multiversion docs/source docs/_build/dirhtml
# Fix for adding 404 page to GitHub
# https://docs.github.com/en/github/working-with-github-pages/creating-a-custom-404-page-for-your-github-pages-site
cd docs/_build/dirhtml
SRC_DIR=$(ls -d *|head -n 1)
ln -sf $SRC_DIR/_static _static
ln -sf $SRC_DIR/404.html 404.html
