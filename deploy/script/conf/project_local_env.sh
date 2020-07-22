#!/bin/bash


# base directory parameters
currentdir=${PWD}
confdir=${currentdir}/../
codedir=${confdir}/../


# deployment directory
deploydir=/tmp/deploy


# data directory
datadir=/tmp/data


# database to backup of path
backup_dir=/tmp/mysql/backup


# docker
docker_compose_file=docker-compose.yml
docker_backup_dir=/var/lib/backup


# invalide project files
invalide_files=(
    "${deploydir}/application/web/src/settings_local.py" 
    "${deploydir}/application/web/src/settings_local.pyc"
)
