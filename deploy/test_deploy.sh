#!/bin/bash

sudo mkdir -p /data
sudo docker-compose -f /deploy/production.yml down
sudo docker rmi deploy_web
sudo rm -rf /deploy/**
sudo cp -rf /project/crm-be/deploy/** /deploy/
sudo cp -rf /project/crm-be/** /deploy/web/
sudo rm -rf /deploy/web/tuoen/settings_local.py
sudo docker-compose -f /deploy/production.yml up -d

sudo chmod -R 774 /data
sudo chmod -R 774 /deploy/nginx/

# 停止10s保证mysql服务启动起来
sleep 10s

##################################################
HOSTNAME="localhost" # 数据库信息
PORT="3306"
USERNAME="root"
PASSWORD="zxcde321BQ"
DBNAME="crm" # 数据库名称

# 创建数据库
create_db_sql="CREATE DATABASE IF NOT EXISTS ${DBNAME} DEFAULT CHARSET utf8 COLLATE utf8_general_ci;"
sudo docker exec deploy_mysql_1 mysql -h${HOSTNAME}  -P${PORT}  -u${USERNAME} -p${PASSWORD} -e "${create_db_sql}"

##################################################

sudo docker exec deploy_web_1 python manage.py migrate
sudo docker exec deploy_web_1 python support/init_manager.py
sudo docker exec deploy_web_1 python support/test_data.py
