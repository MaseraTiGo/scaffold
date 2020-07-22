#!/bin/bash

source ./utils/tools.sh


# initialize flag parameters
if [ "$1" = "online" ]
then
	flag="online"
	log "environment" "to initialize online environment parameters."
	source ./conf/project_online_env.sh
else
	flag="local"
	log "environment" "to initialize test environment parameters."
	source ./conf/project_local_env.sh
fi

# network
sys_network="oc_net"
