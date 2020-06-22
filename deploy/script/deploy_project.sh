#!/bin/bash

source ./clear_project.sh


sudo mkdir -p ${deploydir}
sudo chmod -R 777 ${deploydir}
log "project" "To deploy directory ${deploydir} have been created."

sudo mkdir -p ${datadir}
sudo chmod -R 777 ${datadir}
log "project" "To store data directory ${datadir} have been created."

sudo cp -rf ${confdir}/** ${deploydir}/
sudo cp -rf ${codedir}/** ${deploydir}/application/web/

# if [ "${flag}" = "online" ]
# then
# 	for((i=0;i<${#invalide_files[@]};i++))
# 	do
#         sudo rm -rf ${invalide_files[i]}
#         log "project" "clear ${invalide_files[i]} file of projcet"
# 	done
# fi

for((i=0;i<${#invalide_files[@]};i++))
do
      sudo rm -rf ${invalide_files[i]}
      log "project" "clear ${invalide_files[i]} file of projcet"
done

log "project" "The code have been deployed."


# network
if [[ $(docker network list | grep "${sys_network}" | wc -l) -gt 0 ]]
then 
	log "network" "The ${sys_network} network have existed."
else
	sudo docker network create ${sys_network}
	log "network" "The ${sys_network} network have been initialized."
fi


# add environment
export DEPLOY=${deploydir}
export DATA=${datadir}
