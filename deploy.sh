#!/bin/bash

# Checks if remote origin = original repo
upstream_repo='scylladb/sphinx-scylladb-theme'
origin_repo=$(git config --get remote.origin.url)
if [[ $origin_repo != *$upstream_repo* ]]; then
    echo "Error: You are tring to publish a new version of the theme"\
         "from your personal fork."\
         "Clone the repository '${upstream_repo}' locally,"\
         "then run 'deploy.sh' from the original project."
    exit 1
fi

if git checkout master &&
    git fetch origin master &&
    [ `git rev-list HEAD...origin/master --count` == 0 ] &&
    git merge origin/master
then
    poetry version patch
    poetry build
    poetry publish
else
    echo "Error: Your local repository has some changes not pushed or"\
         "someone has updated the repository while you where editing code."\
         "Upload your latest changes and run  'git pull'."\
         "Then, run 'deploy.sh' again."
fi
