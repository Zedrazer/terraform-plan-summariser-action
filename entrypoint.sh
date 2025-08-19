#!/bin/sh

# When the runner maps the $GITHUB_WORKSPACE mount, it is owned by the runner
# user while the created folders are owned by the container user, causing an
# error. Issue description here: https://github.com/actions/checkout/issues/766
export GIT_PYTHON_REFRESH=quiet
git config --global --add safe.directory /github/workspace

python3 /src/app.py
