#!/bin/bash

FLASKDIR=$(readlink -e "${0%/*}")

echo "Starting $app_name"
echo "$FLASKDIR"

. "$FLASKDIR"/config/settings.ini

# activate the virtualenv
cd $FLASKDIR/$venv_dir
source bin/activate

export PYTHONPATH=$FLASKDIR:$PYTHONPATH


# Start your unicorn
exec gunicorn  server:app --access-logfile $FLASKDIR/var/log/autorisation-access.log --error-log $FLASKDIR/var/log/autorisation-errors.log --pid="${app_name}.pid" -w "${gun_num_workers}" -b "${gun_host}:${gun_port}"  -n "${app_name}"
