#!/bin/bash


# Stop on error.
set -euo pipefail

echo Setup.
pip install httpie
pip install towncrier

echo Checkout master.
git checkout master


echo Checking for changelog items.
python -m towncrier.check || exit 0

echo Configure git.
git config user.name "$GIT_AUTHOR_NAME"
git config user.email "$GIT_AUTHOR_EMAIL"

echo Bump version.
tox -e bump


echo Add remote.
git remote add authorized-origin https://"${GITHUB_TOKEN}"@github.com/"${REPO_OWNER}"/"${REPO_NAME}".git

echo Rebase onto master.
git fetch authorized-origin/master
git rebase authorized-origin/master

echo Push to remote branch.
git push --set-upstream authorized-origin master --follow-tags

echo Release to PyPI.
tox -e release
