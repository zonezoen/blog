> 阅读本文大约需要 7 分钟
## 概述

- MongoDB 的授权访问
- MongoDB 数据集映射到 host 主机
- 第三方授权认证 MongoDB 镜像

## MongoDB 的授权访问 ##
直接上 yml 代码：

```
version: '2'
services:
  mongo-container:
    image: mongo:3.4
    environment:
        # 在这里输入 MongoDB 的 root 用户与密码，如果使用了此项，则不需要 --auth 参数
        - MONGO_INITDB_ROOT_USERNAME=root
        - MONGO_INITDB_ROOT_PASSWORD=rootPass
    ports:
      - "37017:27017"
    volumes:
        # 如果想为特定的数据库创建相应的用户，可以将以下文件映射到容器中，其中创建用户的脚本文件会在下一段代码中
      - "$PWD/mongo-entrypoint/:/docker-entrypoint-initdb.d/"
    command: mongod
```
environment 选项分别表示：（需要说明的是：这是官方支持的）

 1. admin 数据库用户名
 2. admin 数据库密码

下面是创建指定数据库的用户的脚本文件：
```
#!/usr/bin/env bash
echo "Creating mongo users..."
mongo admin --host localhost -u root -p rootPass --eval "db.createUser({user: 'admin', pwd: 'zonePassWord', roles: [{role: 'userAdminAnyDatabase', db: 'admin'}]});"
mongo admin -u root -p rootPass << EOF
use zonedb
db.createUser({user: 'zone', pwd: 'zonePass', roles:[{role:'readWrite',db:'zonedb'}]})
EOF
echo "Mongo users created."
```
那么在这里解释一下创建的过程：

 1. 创建一个 admin 数据库的用户：admin ，密码：zonePassWord ，role：userAdminAnyDatabase
 2. 创建一个 zonedb 数据库的用户：zone ，密码：zonePass ，role：readWrite

## MongoDB 数据集保存至 host 主机 ##
在介绍这个前，得说一下 -v 和 volume，以下这段文字是引用自 [Build Node.Js web server in Docker containers: nodejs+pm2+mongodb+redis](http://blog.csdn.net/dongshaoshuai/article/details/51967133)这篇文章。

> Data volumes 有如下特性：
> 
> 当容器被创建时 volumes 会被初始化 Data volumes 可以在容器间共享复用 对 data volume 的修改直接生效
> 更新镜像时， 原来 data volume 的修改不会被影响 即使容器被删除， 对应的 data volumes 依然会存在 使用
> Volume 可以将容器与容器产生的数据分离，容器产生的数据可以持久化。
> 
> Docker volumes 使用 -v 指定和 在 Dockerfile 指定 VOLUME 的区别：
> 
> -v /data/logs:/data/logs: 将宿主机的 /data/logs 目录挂载到容器的 /data/logs 目录(如果目录不存在会被创建)， 宿主机和容器共享该目录，二者对该目录下的修改相互受影响。 Dockerfile 指定 VOLUME
> /data/logs: 在宿主机创建一个目录(默认是 /var/lib/docker/volumes/)并挂载到容器的 /data/logs
> 目录(如果目录不存在会被创建), 宿主机和容> 器共享该目录，二者对该目录下的修改相互受影响。
> -v /data/logs: 同上， 在宿主机创建一个目录(默认是 /var/lib/docker/volumes/)并挂载到容器的 /data/logs 目录(如果目录不存在会被创建), 宿主机和容器共享该目录，二者对该目录下的修改相互受影响。 Docker
> volumes 默认是 read-write 模式，也可以设置为 read-only 模式。


## 第三方授权认证 MongoDB 镜像 ##
这是一个外国开发者 build 的镜像，已经集成了认证过程。我个人认为数据库这么重要的东西，还是用官方的比较好，但第三方的东西也不妨碍我们学习。那我这边就稍微介绍一下，使用起来还是挺方便的。
[作者原地址](https://hub.docker.com/r/aashreys/mongo-auth/)
```
services:
  db:
    image: aashreys/mongo-auth:latest
    environment:
      - AUTH=yes
      - MONGODB_ADMIN_USER=admin
      - MONGODB_ADMIN_PASS=admin123
      - MONGODB_APPLICATION_DATABASE=sample
      - MONGODB_APPLICATION_USER=aashrey
      - MONGODB_APPLICATION_PASS=admin123
    ports:
      - "27017:27017"
     // more configuration
```
environment 选项分别表示：

 1. 开启认证
 2. admin 数据库用户名
 3. admin 数据库密码
 4. 你使用的工作数据库名称
 5. 工作数据库用户名
 6. 工作数据库密码

至于其他选项就没什么好解释的了。

参考文档如下：
[How to enable authentication on MongoDB through Docker?
](https://stackoverflow.com/questions/34559557/how-to-enable-authentication-on-mongodb-through-docker/45297517#45297517)
[Build Node.Js web server in Docker containers: nodejs+pm2+mongodb+redis](http://blog.csdn.net/dongshaoshuai/article/details/51967133)
[]()


---

## 关注微信公众号，回复【docker资源】，获取 docker 初级视频教程
![zone_qrcode.jpg](http://upload-images.jianshu.io/upload_images/2470773-526cb74252b34bc9?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

