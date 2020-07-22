#!/bin/bash

source ./project_env.sh


#保存备份个数
number=3

#日期
dd=`date +%Y%m%d`


#备份工具
tool=mysqldump

#用户名
username=root
#密码
password=123456

#将要备份的数据库
database_name=oc

# container name
cname=s1


bqcount=`ls -l -crt  $backup_dir/*.sql | awk '{print $9 }' | wc -l`
if [ $bqcount -gt 0 ]
then
    last_backup_file=`ls -l -crt  $backup_dir/*$dd*.sql | awk '{print $9 }' | tail -1`
    end=${last_backup_file#*$dd-}
    index=${end:0:1}
else
    index=0
fi

next_index=`expr $index + 1`
#简单写法 mysqldump -u root -p123456 users > /root/mysqlbackup/users-$filename.sql
sudo docker exec -it $cname /bin/bash -c "$tool -u $username -p$password $database_name > $docker_backup_dir/$database_name-$dd-$next_index.sql"

#写创建备份日志
sudo echo "create $backup_dir/$database_name-$dd.sql" >> $backup_dir/log.txt

#找出需要删除的备份
delfile=`ls -l -crt  $backup_dir/*.sql | awk '{print $9 }' | head -1`

#判断现在的备份数量是否大于$number
count=`ls -l -crt  $backup_dir/*.sql | awk '{print $9 }' | wc -l`


if [ $count -gt $number ]
then
  sudo rm $delfile
  #写删除文件日志
  sudo echo "delete $delfile" >> $backup_dir/log.txt
fi
