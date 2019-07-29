#!/bin/bash


# Stop on error.
set -euo pipefail

echo Setup.
pip install httpie
pip install towncrier


echo Add remote.
git remote remove origin
git remote add origin https://"${GITHUB_TOKEN}"@github.com/"${REPO_OWNER}"/"${REPO_NAME}".git


echo Checkout master.
git fetch --all
git checkout -b master origin/master


echo Checking for changelog items.
python -m towncrier.check || exit 0


echo Configure git.
git config user.name "$GIT_AUTHOR_NAME"
git config user.email "$GIT_AUTHOR_EMAIL"

echo Bump version.
tox -e bump


echo Rebase onto master.
git fetch origin
git rebase origin/master

echo Push to remote branch.
git push --set-upstream origin master --follow-tags

echo Release to PyPI.
tox -e release
