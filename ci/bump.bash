#!/bin/bash

git stash --all
new_version="$(bump2version --dry-run --list patch | grep new_version | sed -r 's/^.*=//')"
towncrier --yes --version="$new_version"
git commit -am'Update changelog with towncrier'
bump2version patch
git stash pop
