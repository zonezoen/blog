# 实战-MySQL定时进行全量与增量备份
## 概要
- 引言
- 全量备份
- 增量备份
- 定时备份
- Docker 中的实现
## 引言
在产品上线之后，我们的数据是相当重要的，容不得半点闪失，应该左后完全的准备，搞不好哪一天被黑客入侵或者恶意删除，那就 gg 了。所以要对我们的线上数据库定时做全量备份与增量备份。例如：每天做一次增量备份，每周做一次全量备份。
## 全量备份
```
#!/bin/bash
#date_now="date +%Y_%n_%d_%H%M"
date_now=$(date "+%Y%m%d-%H%M%S")
backUpFolder=/usr/local/db/backup/mysql
username="root"
password="123qweasd!"
db_name="zone"
fileName="${db_name}_${date_now}.sql"
backUpFileName="${backUpFolder}/${fileName}"
echo $backUpFileName
docker_name="dockercompose_mysql_container_1"
echo $date_now
echo "starting backup mysql ${db_name} at ${date_now}."

#/usr/bin/mysqldump -u${username} -p${password} ${db_name} > ${backUpFileName}
/usr/bin/mysqldump -u${username} -p${password}  --lock-all-tables --flush-logs ${db_name} > ${backUpFileName}
cd ${backUpFolder}
tar zcvf ${fileName}.tar.gz ${fileName}

# use nodejs to upload backup file other place
#NODE_ENV=$backUpFolder@$backUpFileName node /home/imooc_manager/tasks/upload.js

date_end=$(date "+%Y%m%d-%H%M%S")
echo ${date_end}
echo "finish backup mysql database ${db_name} at ${date_end}."
```
## 增量备份
## 定时备份
## Docker 中的实现


