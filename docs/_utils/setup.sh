#!/bin/sh -e

if pwd | egrep -q '\s'; then
	echo "Working directory name contains one or more spaces."
	exit 1
fi

which python3 || { echo "Failed to find python3." && exit 1; }
python3 -m poetry install || { echo "Failed to find poetry: https://python-poetry.org/docs/#installation" && exit 1;}
