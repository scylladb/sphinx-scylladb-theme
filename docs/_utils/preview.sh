#!/bin/sh -e

poetry install
poetry run sphinx-autobuild -a -b html docs/source docs/_build/dirhtml --ignore docs/source/.doctrees/*