#! /usr/bin/env bash

set -e
set -x

alembic upgrade head

python pre_start.py
