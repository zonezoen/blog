## 概述
- 前言
- 什么是 RPC
- RPC 原理
- 常用 RPC 框架对比
- thrift 基础
- python、nodejs 互调
- 后记
## 前言
上一篇文章中，我们初步了解了什么是微服务，那么我们这次来体验一下微服务中是怎么通信的。
## 什么是 RPC
Remote Procedure Call，即为 -- 远程过程调用。通俗地解释一下：你有 A、B 两台电脑，A 电脑用 python 实现了一个加法运算，此时此刻 B 电脑有一个用 Java 实现的程序，想调用 A 电脑的加法运算程序。然而，内存空间不在同一台电脑，且编程语言也不相同，如何调用呢？此时此刻就用网络来表达调用的语义与调用参数。当然，现在我们不用自己去实现这些东西，当下有很多成熟的 RPC 框架供我们选择。

## RPC 原理
什么都别说，先上图。
![RPC 原理](https://upload-images.jianshu.io/upload_images/2470773-3305464ef33b3a65.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
在往下看之前，我们先来了解一下：stub
stub 规定了 server 能够提供什么服务，这在 server 和 client 上是一致的。
**RPC 调用链文字描述：**
(1）client 以本地调用方式调用服务；
(2）client stub 接收到调用后负责将方法、参数等组装成能够进行网络传输的消息体；
(3）client stub 找到服务地址，并将消息发送到服务端；
(4）server stub 收到消息后进行解码；
(5）server stub 根据解码结果调用本地的服务；
(6）server 执行方法并将结果返回给 server stub；
(7）server stub 将返回结果打包成消息并发送至 client；
(8）client stub 接收到消息，并进行解码；
(9）client 得到最终结果。

**RPC 调用链：**
(1)client 发起请求：rpc call --> send --> network
(2)server 接受请求：network --> receive --> local call
(3)server 返回结果：local return --> send --> network
(4)client 接收结果：network --> receive --> rpc return

以上就是 RPC 的原理，需要说明的是，它是同步调用的。

## 常用 RPC 框架对比
RPC 种类 | dubbon | rpcx | grpc | thrift
:-:|:-: | :-: |:-: |:-: |
开发语言 | Java | go | 跨语言 | 跨语言
服务治理 | √ | √ | × | ×
多序列化框架支持 | √ | √ | × | ×
多种注册中心 | √ | √ | × | ×
管理中心 | √ | √ | × | ×
跨语言 | × | × | √ | √ 

一下文字为引用（https://colobu.com/2016/09/05/benchmarks-of-popular-rpc-frameworks/）文章的描述：
> [Dubbo](http://dubbo.io/) 是阿里巴巴公司开源的一个 Java 高性能优秀的服务框架，使得应用可通过高性能的 RPC 实现服务的输出和输入功能，可以和 Spring框架无缝集成。不过，略有遗憾的是，据说在淘宝内部，dubbo 由于跟淘宝另一个类似的框架 HSF（非开源）有竞争关系，导致 dubbo 团队已经解散（参见[http://www.oschina.net/news/55059/druid-1-0-9](http://www.oschina.net/news/55059/druid-1-0-9) 中的评论），反到是当当网的扩展版本仍在持续发展，墙内开花墙外香。其它的一些知名电商如当当、京东、国美维护了自己的分支或者在 dubbo 的基础开发，但是官方的库缺乏维护，相关的依赖类比如 Spring，Netty 还是很老的版本(Spring 3.2.16.RELEASE, netty 3.2.5.Final),倒是有些网友写了升级 Spring 和 Netty 的插件。

> [rpcx](https://github.com/smallnest/rpcx) 是Go语言生态圈的 Dubbo， 比 Dubbo 更轻量，实现了 Dubbo 的许多特性，借助于Go语言优秀的并发特性和简洁语法，可以使用较少的代码实现分布式的 RPC 服务。

> [gRPC](http://www.grpc.io/) 是 Google 开发的高性能、通用的开源 RPC 框架，其由 Google 主要面向移动应用开发并基于 HTTP/2 协议标准而设计，基于 ProtoBuf(Protocol Buffers) 序列化协议开发，且支持众多开发语言。本身它不是分布式的，所以要实现上面的框架的功能需要进一步的开发。

> [thrift](https://thrift.apache.org/) 是 Apache 的一个跨语言的高性能的服务框架，基于 thrift 进行序列化。也得到了广泛的应用。

其中比较受关注的是：**grpc 与 thrift 。**
**grpc 支持的语言：**C++,C#,Dart,Go,Java,Node.js,Objective-C,PHP,Python,Ruby,
**thrift 支持的语言：**C++, Java, Python, PHP, Ruby, Erlang, Perl, Haskell, C#, Cocoa, JavaScript, Node.js, Smalltalk, OCaml and Delphi 等

## thrift 基础
实现两门语言的相互调用，这里选用 thrift 框架，接下来会简单介绍一下 thrift 的用法，并编码实现一个 python 与 nodejs 互相调用的程序。下面简单介绍下 thrift 语法。
基本数据类型：
```
bool: 布尔类型(true / false)

byte: 8位带符号整数

i16: 16位带符号整数

i32: 32位带符号整数

i64: 64位带符号整数

double: 64位浮点数

string: 采用UTF-8编码的字符串

map<t1,t2> 键值对

list<t1> 列表

set<t1> 集合
```

结构：
```
struct User {
1: i32 uid,
2: string name,
3: string age,
4: string sex
}
```
service，对外扩展的接口：
```
service UserStorage {
void addUser(1: User user),
User getUser(1: i32 uid)
}
```
最后，使用 thrift 命令生成相应的接口文件：
```
thrift -out ../python --gen py test.thrift
thrift -out 存储路径 --gen 接口语言 thrift 文件名
```

## python、nodejs 互调
OK，语法差不多都熟悉了，那么我们来实践一下：
![项目结构图](https://upload-images.jianshu.io/upload_images/2470773-900bc4538cb675de.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
其中绿色框框为我们自己新建的代码，红色框框为 thrift 生成的代码，我们调用就行。
我们先来看互相调用的结果：
**先看看 python 为服务端，nodejs 为客户端的调用情况：**
![python 服务端](https://upload-images.jianshu.io/upload_images/2470773-a1940354085319f6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![nodejs 客户端](https://upload-images.jianshu.io/upload_images/2470773-c2cd7575d73c81ea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在看看，nodejs 为服务端，python 为客户端的情况：
![nodejs 服务端](https://upload-images.jianshu.io/upload_images/2470773-88d6e1c64e4f98f7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![python 客户端](https://upload-images.jianshu.io/upload_images/2470773-7041a09878271ee8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#### createThrift.sh
```
#!/bin/bash
cd thrift
thrift -out ../nodejs --gen js:node test.thrift
thrift -out ../python --gen py test.thrift
```
#### test.thrift
生成红色框框的 thrift 接口代码文件。
```
struct Student{
1: string name,
2: string age
}
service UserService{
     void addStu(1: Student stu),
     Student getStu(1: string name)
}
```
#### python server
```
from python.test import UserService
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
stus = {}
class TestHandler:
    def addStu(self, stu):
        print("我是 python 服务器，我的 addStu() 方法被调用了.")
        stus[stu.name] = stu
        # print("add new student : " + stu.name)

    def getStu(self, name):
        print("我是 python 服务器，我的 getStu() 方法被调用了.")
        print("get student : " + name)
        return stus[name]

# 创建服务端
handler = TestHandler()
processor = UserService.Processor(handler)
# 监听端口
transport = TSocket.TServerSocket("127.0.0.1", 3000)
# 选择传输层
tfactory = TTransport.TBufferedTransportFactory()
# 选择传输协议
pfactory = TBinaryProtocol.TBinaryProtocolFactory()
# 创建服务端
server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
print("Starting thrift server in python...")
server.serve()
```
#### python client
```
from python.test import UserService
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

__HOST = '127.0.0.1'
__PORT = 3000
tsocket = TSocket.TSocket(__HOST, __PORT)
transport = TTransport.TBufferedTransport(tsocket)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
# 穿件客户端
client = UserService.Client(protocol)
# thrift 生成的的 Student 结构
stu = UserService.Student("zone", "18")
transport.open()
# 调用服务端 addStu() 方法
print("我是 python 客户端，我调用了 addStu() 方法.")
client.addStu(stu)
# 调用服务端 getStu() 方法
print("我是 python 客户端，我调用了 getStu() 方法.")
print("返回的结果为：" + client.getStu("zone"))
transport.close()
```
#### nodejs server
```
var thrift = require("thrift");
var UserService = require('../UserService.js');
var ttypes = require('../test_types');

var stus = {}
var server = thrift.createServer(UserService,
    {
        addStu: function (stu, callback) {
            console.log("我是 nodejs 服务器，我的 addStu() 方法被调用了.");
            stus[stu.name] = stu
            console.log(stu);
            callback();
        },
        getStu: function (name, callback) {
            console.log("我是 nodejs 服务器，我的 getStu() 方法被调用了.");
            callback(null, stus[name])
        }
    }
);
// 启动服务
server.listen(3000);
console.log("nodejs server start");
server.on("error", function (e) {
    console.log(e);
});
```
#### nodejs client
```
var thrift = require('thrift');
var UserService = require('../UserService.js');
var ttypes = require('../test_types');

var connection = thrift.createConnection('127.0.0.1', 3000);
var client = thrift.createClient(UserService, connection);
connection.on("error", function (e) {
    console.log(e);
});
var stu = new ttypes.Student({name: "zone-nodejs", age: "23"});
// 调用服务端 addStu() 方法
client.addStu(stu, function (err, res) {
    if (err) {
        console.log(err);
        return
    }
    console.log("我是 nodejs 客户端，我调用了 addStu() 方法.")
})
// 调用服务端 getStu() 方法
client.getStu("zone-nodejs", function (err, res) {
    if (err) {
        console.log(err);
        return
    }
    console.log("我是 nodejs 客户端，我调用了 getStu() 方法.")
    console.log("返回的结果为：" + res)
})
```
## 后记
微服务中，RPC 框架的性能是很重要的，因为一旦要做微服务，就是成百上千个微服务的，这涉及到各个微服务之间的通信问题。通信慢了，那么整体的响应速度也就相对慢很多了。下一篇文章讲一下消息队列，敬请期待！

