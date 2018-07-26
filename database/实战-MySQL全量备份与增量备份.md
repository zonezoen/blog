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
http://a.com
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
#获取当前时间
date_now=$(date "+%Y%m%d-%H%M%S")
backUpFolder=/home/db/backup/mysql
username="root"
password="123456"
db_name="zone"
fileName="${db_name}_${date_now}.sql"
backUpFileName="${backUpFolder}/${fileName}"
echo "starting backup mysql ${db_name} at ${date_now}."

#/usr/bin/mysqldump -u${username} -p${password} ${db_name} > ${backUpFileName}
/usr/bin/mysqldump -u${username} -p${password}  --lock-all-tables --flush-logs ${db_name} > ${backUpFileName}
cd ${backUpFolder}
tar zcvf ${fileName}.tar.gz ${fileName}

# use nodejs to upload backup file other place
#NODE_ENV=$backUpFolder@$backUpFileName node /home/tasks/upload.js
date_end=$(date "+%Y%m%d-%H%M%S")
echo "finish backup mysql database ${db_name} at ${date_end}."
```
## 恢复全量备份



## 增量备份

```shell
#!/bin/bash
# Program
# use cp to backup mysql data everyday!
# History
# Path
BakDir=/usr/local/work/backup/daily
#//增量备份时复制mysql-bin.00000*的目标目录，提前手动创建这个目录
BinDir=/var/lib/mysql
#//mysql的数据目录
LogFile=/usr/local/work/backup/bak.log
BinFile=/var/lib/mysql/mysql-bin.index
#//mysql的index文件路径，放在数据目录下的



mysqladmin -uroot -p123qweasd! flush-logs
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
## Docker 中的实现


