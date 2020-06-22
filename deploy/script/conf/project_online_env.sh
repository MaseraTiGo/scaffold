#!/bin/bash


# base directory parameters
currentdir=${PWD}
confdir=${currentdir}/../
codedir=${confdir}/../

# deployment directory
deploydir=/deploy


# data directory
datadir=/data


# database to backup of path
backup_dir=/data/databases/mysql-master/backup


# docker
docker_compose_file=online_production.yml
docker_backup_dir=/var/lib/backup


# invalide project files
invalide_files=(
    "${deploydir}/application/web/tuoen/settings_local.py" 
    "${deploydir}/application/web/tuoen/settings_local.pyc"
)
