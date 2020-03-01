#!/bin/sh -e

if pwd | egrep -q '\s'; then
	echo "Working directory name contains one or more spaces."
	exit 1
fi

which virtualenv\
||(which brew && brew install python && pip install virtualenv)\
||(which dnf && sudo dnf install python-virtualenv)\
||(which apt-get && sudo apt-get install python-virtualenv)

which virtualenv || echo "Failed to find or install virtualenv."
which python3 || { echo "Failed to find python3." && exit 1; }
# set up virtualenv and Sphinx
virtualenv -p python3 . || exit 1
. bin/activate
export PATH="./bin:$PATH"
[ -x bin/sphinx-build ] || pip install -v pyyaml livereload recommonmark sphinx-tabs sphinx-copybutton 'sphinx==1.8.0'
