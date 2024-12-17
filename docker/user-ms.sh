#!/bin/bash
python /code/src/user_ms/manage.py migrate --check
status=$?
if [[ $status != 0 ]]; then
  python /code/src/user_ms/manage.py migrate
fi
exec "$@"