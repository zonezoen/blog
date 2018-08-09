## 概要
- 引言
- 回顾
- 备份到私有云-python
- 备份到私有云-nodejs
- 备份到git私有仓库

# 引言
传送门：

[实战-MySQL定时全量备份（1）](https://mp.weixin.qq.com/s/I4tLPuzcnHMA9crChDXEeQ)

[实战-MySQL定时增量备份（2）](https://mp.weixin.qq.com/s/ynIyK7Fb8ayziTV3wAFjCg)

前两篇文章聊了 MySQL 的全量备份与增量备份，我们也学会了数据库的备份与恢复。这也增强了我们数据库的安全性。假如，我们整台数据库服务器被劫持了，或者遇到了其他毁灭性的灾难，即使备份了也没个毛用，因为备份文件也在同一台服务器啊。那么我们就会想如何备份的同时，上传到其他私有云，这样我们就不用担心了。于是便有了本文。
## 回顾

OK，学习了上两篇文章，我们已经可以轻松地备份数据库，也得到了以下脚本文件。而在下面脚本的最后几行，我添加了几行将备份文件上传到私有云的代码。这里我注释掉了，如要使用请取消注释。OK，现在让我们一起打怪升级。

```shell
#!/bin/bash
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
# 使用 nodejs 上传备份文件到 私有云
#NODE_ENV=$backUpFolder@$backUpFileName /root/node/v8.11.3/bin/node /usr/local/upload.js

# 使用 python 上传备份文件到 私有云
#python /use/local/upload.py $backUpFolder $backUpFileName
```


```Shell
# 使用 python 上传备份文件到 私有云
#python /use/local/upload.py $backUpFolder $backUpFileName
```

```shell
$backUpFolder #备份文件的所在目录
$backUpFileName #备份文件名
```

这两个参数为传给 upload.py 的参数。

```Shell
# 使用 nodejs 上传备份文件到 私有云
#/root/node/v8.11.3/bin/node /usr/local/upload.js $backUpFolder $backUpFileName
```

这两个参数为传给 upload.js 的参数。

##备份到私有云-python

这里的私有云使用的是七牛云，使用其他私有云请自行替换。以下脚本中，替换你自己的 access_key、secret_key、bucket_name（存储仓库名）  即可使用。


```python
from qiniu import Auth, put_file, etag
import sys
print('参数个数为:', len(sys.argv), '个参数。')
print('参数列表:', str(sys.argv))

# backUpFolder,获取备份文件的目录
backUpFolder = sys.argv[1]
# backUpFileName，获取备份文件的文件名
backUpFileName = sys.argv[2]
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = 'your_key'
secret_key = 'your_key'
# 构建鉴权对象
q = Auth(access_key, secret_key)
# 要上传的空间
bucket_name = 'test'
# 上传到七牛后保存的文件名
key = backUpFileName
# 生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)
# 要上传文件的本地路径
localfile = backUpFolder + backUpFileName
ret, info = put_file(token, key, localfile)
print(info)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)

```

## 备份到私有云-nodejs

这里的私有云使用的是七牛云，使用其他私有云请自行替换。以下脚本中，替换你自己的 access_key、secret_key、bucket（存储仓库名）  即可使用。

```javascript
let qiniu = require("qiniu");
let arguments = process.argv.splice(2);
console.log(process.argv)
console.log('所传递的参数是：', arguments[0]);
console.log('所传递的参数是：', arguments[1]);
let file = arguments[1];
let filePath = arguments[0] + '/' + file;
console.log(filePath);
bucket = "test"//你的存储空间名

//需要填写你的 Access Key 和 Secret Key
let accessKey = 'access_key';
let secretKey = 'secret_key';


let config = new qiniu.conf.Config();
// 空间对应的机房，选择机房得看七牛的文档：https://developer.qiniu.com/kodo/sdk/1289/nodejs#form-upload-file
config.zone = qiniu.zone.Zone_z0;
let mac = new qiniu.auth.digest.Mac(accessKey, secretKey);
let options = {
    scope: bucket,
};
let putPolicy = new qiniu.rs.PutPolicy(options);
let uploadToken=putPolicy.uploadToken(mac);


let localFile = filePath;
let formUploader = new qiniu.form_up.FormUploader(config);
let putExtra = new qiniu.form_up.PutExtra();
let key = file;
// 文件上传
formUploader.putFile(uploadToken, key, localFile, putExtra, function (respErr, respBody, respInfo) {
    if (respErr) {
        throw respErr;
    }
    if (respInfo.statusCode == 200) {
        console.log(respBody);
    } else {
        console.log(respInfo.statusCode);
        console.log(respBody);
    }
});
```

![image-20180804160927893](/var/folders/6t/zbv9qpzs3ks_7xpv5skkgkt40000gp/T/abnerworks.Typora/image-20180804160927893.png)

上图为我本地运行脚本文件上传 README.md 的截图。上传成功。

## 备份到git私有仓库

github 中的私有仓库需要付费，可以选择码云来作为私有仓库，其私有仓库的免费的。

```shell
#!/bin/bash
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

git add .
git commit -m 'commit by script'
git push
```



