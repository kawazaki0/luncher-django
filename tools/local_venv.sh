#!/usr/bin/env bash
set -xe 

python3 -m venv --clear "$(git rev-parse --show-toplevel)/.venv"

# shellcheck disable=SC1090
source "$(git rev-parse --show-toplevel)/.venv/bin/activate"
pip install --upgrade pip==19.0.3
pip install -r requirements/local.txt
