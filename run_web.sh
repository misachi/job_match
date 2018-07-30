#!/usr/bin/env bash

set -e

# create access log file
LOG_FILES='log_files'
ACCESS_LOG_FILE="${LOG_FILES}/gunicorn_access.logs"
ERROR_LOG_FILE="${LOG_FILES}/gunicorn_error.logs"

if [ ! -d ${LOG_FILES} ]; then
    mkdir ${LOG_FILES}
fi

if [ ! -f ${ACCESS_LOG_FILE} ]; then
    touch ${ACCESS_LOG_FILE}
fi

if [ ! -f ${ERROR_LOG_FILE} ]; then
    touch ${ERROR_LOG_FILE}
fi

# Run gunicorn server
/usr/local/bin/gunicorn --access-logfile=${ACCESS_LOG_FILE} --error-logfile=${ERROR_LOG_FILE} --access-logformat="%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s" --log-level=error --env DJANGO_SETTINGS_MODULE=jobs.settings jobs.wsgi:application -w 2 -b :8010