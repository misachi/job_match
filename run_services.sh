#!/usr/bin/env bash

COMPOSE_FILE='docker-compose.yml'

if [ ! -f ${COMPOSE_FILE} ]; then
    echo "${COMPOSE_FILE} does not exist"
    exit
fi

docker-compose up -d