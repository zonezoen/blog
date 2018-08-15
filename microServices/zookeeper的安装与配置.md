## 概述
- 什么是 zookeeper
- zookeeper 的安装与配置
- 运行 zookeeper
- 单机集群
- 多机集群
- Docker 实现 zookeeper 集群

## 什么是 zookeeper
先用通俗的语言说一下。编程语言的命名通常比较有戏剧性。有以动物命名的，也有食物命名的。

zookeeper：意思是动物园饲养员

Tomcat：是一只猫

Hadoop：是一只黄色的大象

Python：是一条蟒蛇

Apache pig：是一只猪

总的来说，zookeeper 是管理这些东西的。具体怎么管理？且看详细解释。

```

Apache ZooKeeper
开发者	Apache软件基金会
稳定版本	
3.4.10 （2017年3月30日，​15个月前 ）
预览版本	
3.5.3-beta （2017年4月17日，​15个月前 ）
编程语言	Java
操作系统	跨平台
类型	分布式计算
许可协议	Apache许可证 2.0
网站	zookeeper.apache.org
Apache ZooKeeper是Apache软件基金会的一个软件项目，他为大型分布式计算提供开源的分布式配置服务、同步服务和命名注册。[需要解释] ZooKeeper曾经是Hadoop的一个子项目，但现在是一个独立的顶级项目。

ZooKeeper的架构通过冗余服务实现高可用性。因此，如果第一次无应答，客户端就可以询问另一台ZooKeeper主机。ZooKeeper节点将它们的数据存储于一个分层的命名空间，非常类似于一个文件系统或一个前缀树结构。客户端可以在节点读写，从而以这种方式拥有一个共享的配置服务。更新是全序的。[1]
```

## zookeeper 的安装与配置
- 首先到官网下载 [zookeeper-stable](http://mirrors.hust.edu.cn/apache/zookeeper/stable/zookeeper-3.4.12.tar.gz)
- 解压得到如下目录
![zookeeper 解压目录](https://upload-images.jianshu.io/upload_images/2470773-5b3b3f9da06d3f54.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
> bin 目录存放 zookeeper 启动文件 
> lib 目录存放 zookeeper 的第三方库
> conf 目录存放 zookeeper 的配置文件
- cd 进入 conf 目录，新建文件 zoo.cfg
- 添加以下配置
```
tickTime=2000  
dataDir=/usr/your/path/data  
dataLogDir=/usr/your/path/logs 
clientPort=2181
```
> tickTime：zookeeper 中使用的基本时间单位，毫秒值
> dataDir：zookeeper 的数据目录
> dataLogDir：zookeeper 的 log 目录
> clientPort：zookeeper 的运行端口

## 运行 zookeeper 
配置完成之后，回到 zookeeper 解压目录。
#### 后台运行
```
./bin/zkServer.sh start
```
![image.png](https://upload-images.jianshu.io/upload_images/2470773-ce6081014e6a9e30.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
#### 停止运行
```
./bin/zkServer.sh stop
```

#### 前台运行
```
./bin/zkServer.sh start-foreground
```
![image.png](https://upload-images.jianshu.io/upload_images/2470773-7ec833865dac6cc6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 单机集群
单机集群即是在一台机子上的伪集群。要做集群，则需要将不同 zookeeper 实例的配置文件放到不同的文件夹。

myid | data 目录 | port | server | leader | conf
---|---|---|---|---|---
1 | /usr/your/path/z1/z1.cfg | 2181 | 2222 | 2223 | z1.cfg
2 | /usr/your/path/z2/z2.cfg | 2182 | 3333 | 3334 | z2.cfg
3 | /usr/your/path/z3/z3.cfg | 2184 | 4444 | 4445 | z3.cfg

我的目录文件为，/usr/your/path/z1/data ，则在该目录下新建文件
```
vim myid
```
录入值
```
1
```
请分别对应表格中的值，在不同的目录创建 myid 文件。

z1.cfg
```
tickTime=2000
initLimit=10
syncLimit=2
dataDir=/usr/your/path/z1/data
clientPort=2181
server.1=127.0.0.1:2222:2225
server.2=127.0.0.1:3333:3335
server.3=127.0.0.1:4444:4445
```
z2.cfg
```
tickTime=2000
initLimit=10
syncLimit=2
dataDir=/usr/your/path/z2/data
clientPort=2182
server.1=127.0.0.1:2222:2225
server.2=127.0.0.1:3333:3335
server.3=127.0.0.1:4444:4445
```
z3.cfg
```
tickTime=2000
initLimit=10
syncLimit=2
dataDir=/usr/your/path/z3/data
clientPort=2183
server.1=127.0.0.1:2222:2225
server.2=127.0.0.1:3333:3335
server.3=127.0.0.1:4444:4445
```



配置文件弄好之后，分别启动不同的实例。命令行如下：
```
./bin/zkServer.sh start /usr/your/path/z1/z1.cfg
./bin/zkServer.sh start /usr/your/path/z2/z2.cfg
./bin/zkServer.sh start /usr/your/path/z3/z3.cfg
```
启动完毕之后，运行 zookeeper 命令行客户端
```
bin/zkCli.sh -server 127.0.0.1:2181,127.0.0.1:2182,127.0.0.1:2183  
```
运行结果如图：

![image.png](https://upload-images.jianshu.io/upload_images/2470773-9b265bf28417252f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## Docker 实现 zookeeper 集群
```
version: '2'
services:
    zoo1:
        image: zookeeper
        restart: always
        ports:
            - 2181:2181
        environment:
            ZOO_MY_ID: 1
            ZOO_SERVERS: server.1=zoo1:2888:3888 server.2=zoo2:2888:3888 server.3=zoo3:2888:3888

    zoo2:
        image: zookeeper
        restart: always
        ports:
            - 2182:2181
        environment:
            ZOO_MY_ID: 2
            ZOO_SERVERS: server.1=zoo1:2888:3888 server.2=zoo2:2888:3888 server.3=zoo3:2888:3888

    zoo3:
        image: zookeeper
        restart: always
        ports:
            - 2183:2181
        environment:
            ZOO_MY_ID: 3
            ZOO_SERVERS: server.1=zoo1:2888:3888 server.2=zoo2:2888:3888 server.3=zoo3:2888:3888


```
