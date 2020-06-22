#!/bin/bash

source ./stop_project.sh


if [ -e ${deploydir} ]
then
	sudo rm -rf ${deploydir}
	log "project" "${deploydir} have been removed."
fi
