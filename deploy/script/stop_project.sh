#!/bin/bash

source ./project_env.sh


log "server" "to stop project is starting ..."
if [ -e ${deploydir} ]
then
	server_names=('mycat' 'mysql' 'rabbitmq' 'redis' 'web' 'nginx')
	server_path=('/middleware/mycat' '/database/mysql' '/middleware/rabbitmq' '/cache/redis' '/application/web' '/balance/nginx')

	server_len=${#server_names[@]} 
	for((i=0;i<${server_len};i++))
	do
                cd ${deploydir}${server_path[i]}
                sudo docker-compose -f ${docker_compose_file} down
	done
else
	log "server" "${deploydir} is not existed, it is not need to stop."
fi
log "server" "to stop project have finished ..."
