# 实战-MySQL定时进行全量与增量备份
## 概要
- 引言
- 全量备份
- 恢复全量备份
- 增量备份
- 恢复增量备份
- 定时备份
- Docker 中的实现
## 引言
在产品上线之后，我们的数据是相当重要的，容不得半点闪失，应该做好万全的准备，搞不好哪一天被黑客入侵或者恶意删除，那就 gg 了。所以要对我们的线上数据库定时做全量备份与增量备份。例如：每天做一次增量备份，每周做一次全量备份。

GitHub 地址：

```
https://github.com/zonezoen/MySQL_backup
```



## 全量备份

```sh
/usr/bin/mysqldump -uroot -p123456  --lock-all-tables --flush-logs test > /home/backup.sql
```

如上一段代码所示，其功能是将 test 数据库全量备份。其中 MySQL 用户名为：root ，密码为：123456。备份的文件路径为：/home ，当然这个路径也是可以按照个人意愿修改的。备份的文件名为 backup.sql

参数 —flush-logs：使用一个新的日志文件来记录接下来的日志；

参数 —lock-all-tables：锁定所有数据库;

**以下为我使用的脚本文件：**

脚本文件功能不是很复杂，首先是各种变量赋值。然后备份数据库，接着是进入到备份文件所在的目录，再将备份文件压缩。**其中倒数第三行是使用 nodejs 将备份的文件上传到七牛云中，这里就不在过多的阐述了，与本文主题不符，想看具体实现可以查看 GitHub 源码。**

```shell
#!/bin/bash
#在使用之前，请提前创建以下各个目录
#获取当前时间
date_now=$(date "+%Y%m%d-%H%M%S")
backUpFolder=/home/db/backup/mysql
username="root"
password="123456"
db_name="zone"
#定义备份文件名
fileName="${db_name}_${date_now}.sql"
#定义备份文件目录
backUpFileName="${backUpFolder}/${fileName}"
echo "starting backup mysql ${db_name} at ${date_now}."
/usr/bin/mysqldump -u${username} -p${password}  --lock-all-tables --flush-logs ${db_name} > ${backUpFileName}
#进入到备份文件目录
cd ${backUpFolder}
#压缩备份文件
tar zcvf ${fileName}.tar.gz ${fileName}

# use nodejs to upload backup file other place
#NODE_ENV=$backUpFolder@$backUpFileName node /home/tasks/upload.js
date_end=$(date "+%Y%m%d-%H%M%S")
echo "finish backup mysql database ${db_name} at ${date_end}."
```
## 恢复全量备份

```shell
mysql -h localhost -uroot -p123456 < bakdup.sql
```

或者

```shell
mysql> source /path/backup/bakdup.sql
```

嗯，回复全量备份也就这样两句，似乎不用多说什么了。对了，在恢复全量备份之后，要将全量备份之后的增量备份也恢复回数据库中。

## 增量备份

首先在进行增量备份之前需要查看一下配置文件，查看 log_bin 是否开启，因为要做增量备份首先要开启 log_bin 。首先，进入到 myslq 命令行，输入如下命令：

```shell
show variables like '%log_bin%';
```

如下命令所示，则为未开启

```
mysql> show variables like '%log_bin%';
+---------------------------------+-------+
| Variable_name                   | Value |
+---------------------------------+-------+
| log_bin                         | OFF   |
| log_bin_basename                |       |
| log_bin_index                   |       |
| log_bin_trust_function_creators | OFF   |
| log_bin_use_v1_row_events       | OFF   |
| sql_log_bin                     | ON    |
+---------------------------------+-------+
```

修改 MySQL 配置项到如下代码段：vim /etc/mysql/mysql.conf.d/mysqld.cnf 

```
# Copyright (c) 2014, 2016, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

#
# The MySQL  Server configuration file.
#
# For explanations see
# http://dev.mysql.com/doc/mysql/en/server-system-variables.html

[mysqld]
pid-file	= /var/run/mysqld/mysqld.pid
socket		= /var/run/mysqld/mysqld.sock
datadir		= /var/lib/mysql
#log-error	= /var/log/mysql/error.log
# By default we only accept connections from localhost
#bind-address	= 127.0.0.1
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

#binlog setting，开启增量备份的关键
log-bin=/var/lib/mysql/mysql-bin
server-id=123454
```

修改之后，重启 mysql 服务，输入：

```shell
show variables like '%log_bin%';
```

状态如下：

```shell
mysql> show variables like '%log_bin%';
+---------------------------------+--------------------------------+
| Variable_name                   | Value                          |
+---------------------------------+--------------------------------+
| log_bin                         | ON                             |
| log_bin_basename                | /var/lib/mysql/mysql-bin       |
| log_bin_index                   | /var/lib/mysql/mysql-bin.index |
| log_bin_trust_function_creators | OFF                            |
| log_bin_use_v1_row_events       | OFF                            |
| sql_log_bin                     | ON                             |
+---------------------------------+--------------------------------+
```

好了，做好了充足的准备，那我们就开始学习增量备份了。

查看当前使用的 mysql_bin.000*** 日志文件，

```shell
show master status;
```

状态如下：

```shell
mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000015 |      610 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
```

当前正在记录日志的文件名为 mysql-bin.000015 。

当前数据库中有如下数据：

```shell
mysql> select * from users;
+-------+------+----+
| name  | sex  | id |
+-------+------+----+
| zone  | 0    |  1 |
| zone1 | 1    |  2 |
| zone2 | 0    |  3 |
+-------+------+----+
```

我们插入一条数据：

```mysql
insert into `zone`.`users` ( `name`, `sex`, `id`) values ( 'zone3', '0', '4');
```

查看效果：

```shell
mysql> select * from users;
+-------+------+----+
| name  | sex  | id |
+-------+------+----+
| zone  | 0    |  1 |
| zone1 | 1    |  2 |
| zone2 | 0    |  3 |
| zone3 | 0    |  4 |
+-------+------+----+
```

我们执行如下命令，使用新的日志文件：

```shell
mysqladmin -uroot -123456 flush-logs
```

日志文件从 mysql-bin.000015 变为  mysql-bin.000016，而 mysql-bin.000015 则记录着刚刚 insert 命令的日志。上句代码的效果如下：

```
mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000016 |      154 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
```

那么到现在为止，其实已经完成了增量备份了。

## 恢复增量备份

那么现在将刚刚插入的数据删除，效果如下：

```mysql
delete from `zone`.`users` where `id`='4' 
```

```mysql
mysql> select * from users;
+-------+------+----+
| name  | sex  | id |
+-------+------+----+
| zone  | 0    |  1 |
| zone1 | 1    |  2 |
| zone2 | 0    |  3 |
+-------+------+----+
```

那么现在就是重点时间了，从 mysql-bin.000015 中恢复数据：

```shell
mysqlbinlog /var/lib/mysql/mysql-bin.000015 | mysql -uroot -p123456 zone;
```

上一句代码指定了，需要恢复的 mysql_bin 文件，指定了用户名：root 、密码：123456 、数据库名：zone。效果如下：

```mysql
mysql> select * from users;
+-------+------+----+
| name  | sex  | id |
+-------+------+----+
| zone  | 0    |  1 |
| zone1 | 1    |  2 |
| zone2 | 0    |  3 |
| zone3 | 0    |  4 |
+-------+------+----+
```

OK，整一个增量备份的操作流程都在这里了，那么我们如何将它写成脚本文件呢，代码如下：

```shell
#!/bin/bash
#在使用之前，请提前创建以下各个目录
BakDir=/usr/local/work/backup/daily
#增量备份时复制mysql-bin.00000*的目标目录，提前手动创建这个目录
BinDir=/var/lib/mysql
#mysql的数据目录
LogFile=/usr/local/work/backup/bak.log
BinFile=/var/lib/mysql/mysql-bin.index
#mysql的index文件路径，放在数据目录下的

mysqladmin -uroot -p123456 flush-logs
#这个是用于产生新的mysql-bin.00000*文件
# wc -l 统计行数
# awk 简单来说awk就是把文件逐行的读入，以空格为默认分隔符将每行切片，切开的部分再进行各种分析处理。
Counter=`wc -l $BinFile |awk '{print $1}'`
NextNum=0
#这个for循环用于比对$Counter,$NextNum这两个值来确定文件是不是存在或最新的
for file in `cat $BinFile`
do
    base=`basename $file`
    echo $base
    #basename用于截取mysql-bin.00000*文件名，去掉./mysql-bin.000005前面的./
    NextNum=`expr $NextNum + 1`
    if [ $NextNum -eq $Counter ]
    then
        echo $base skip! >> $LogFile
    else
        dest=$BakDir/$base
        if(test -e $dest)
        #test -e用于检测目标文件是否存在，存在就写exist!到$LogFile去
        then
            echo $base exist! >> $LogFile
        else
            cp $BinDir/$base $BakDir
            echo $base copying >> $LogFile
         fi
     fi
done
echo `date +"%Y年%m月%d日 %H:%M:%S"` $Next Bakup succ! >> $LogFile

#NODE_ENV=$backUpFolder@$backUpFileName /root/.nvm/versions/node/v8.11.3/bin/node /usr/local/work/script/upload.js

```



## 定时备份

输入如下命令，进入定时任务编辑界面：

```shell
crontab -e
```

添加如下命令，其意思为：每分钟执行一次备份脚本，crontab 的具体规则就另外写文了，与本文主题不太相关。

```
* * * * * sh /usr/your/path/mysqlbackup.sh
```



## Docker 中的实现

在 Docker 中实现，其实也是差多的，我就不在将上面的步骤重新赘述一遍了，我就直接将我在 Docker 中遇到的坑展示给大家吧。

### 安装 vim

我使用的是 MySQL 的官方镜像，Docker - MySQL 镜像中使用的事 Debian 系统，其版本比较老旧是，没有佩带 vim 的。首先我们要执行以下代码来安装 vim ：

```shell
apt-get update
```

```
apt-get install vim
```

安装好 vim 之后，就可以愉快地编辑 vim /etc/mysql/mysql.conf.d/mysqld.cnf  了。忘了提一点，这个文件是不能映射到容器里面的，因为容器里面本身有这个文件。

### 修改时区

在我们备份数据库的时候，有用到时间因素，但是 Docker 容器中默认为 +0 时区，而我们是 +8 时区，我们将宿主机的时区文件映射过去就行。

```
-v /etc/localtime:/etc/localtime:ro
```

也可以通过进入容器来修改时区，这个就看个人选择了，具体修改方法博客地址里面：http://coolnull.com/235.html

###  定时备份

在容器中如何实现定时备份呢？有人会说，使用 crontab 呀？如果你是这么想的，那么很遗憾，在 Docker - MySQL 的官方镜像中是没有 crontab 的。有人又说，那我们装一个 crontab不就行了吗？但是 Docker 鼓励“一个容器一个进程(one process per container)”的方式。于是在查找资料无果之后，我转念一想，将定时任务分配到我们的宿主机不就行了？让宿主机定时往容器里面传递命令，就达到我们的目的了。

输入如下命令，进入定时任务编辑界面：

```shell
crontab -e
```

添加如下命令，其内容为：每分钟执行一次备份脚本

```shell
* * * * * docker exec ${docker_name} /bin/sh /usr/your/path/mysqlbackup.sh
```



