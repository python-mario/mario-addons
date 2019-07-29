#!/bin/bash

set -euo pipefail

git stash --all
new_version="$(bump2version --dry-run --list patch | grep new_version | sed -r 's/^.*=//')"
towncrier --yes --version="$new_version"
bump2version --allow-dirty --new-version="$new_version" patch
git stash pop
