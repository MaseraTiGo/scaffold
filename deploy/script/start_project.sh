#!/bin/bash

source ./deploy_project.sh


log "server" "to start project is starting ..."
if [ -e ${deploydir} ]
then
	server_names=('mysql' 'mycat' 'rabbitmq' 'redis' 'web' 'nginx')
	server_path=('/database/mysql' '/middleware/mycat' '/middleware/rabbitmq' '/cache/redis' '/application/web' '/balance/nginx')

	server_len=${#server_names[@]} 
	for((i=0;i<${server_len};i++))
	do
		cd ${deploydir}${server_path[i]}
		sudo docker-compose -f ${docker_compose_file} up -d
	done
else
	log "server" " ${deploydir} is not existed, to deploy is failed!"
fi
log "server" "to start project have finished ..."
