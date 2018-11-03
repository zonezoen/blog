## 概述
- 前言
- 源码
- registrator
- API gateway
- web 服务
- 运行
- 后记
## 前言
这篇文章真是等了挺久才写，让小伙伴们久等了。这篇文章旨在带你走一下微服务的流程，真实的微服务远不止这些东西。详细的介绍敬请关注我后面的文章。**如果我的文章对你有帮助，欢迎关注、点赞、转发，这样我会更有动力做原创分享。**OK，进入正题！
## 源码
首先甩出源码吧，因为这对于刚接触的小伙伴来说这可能还是个庞然大物。先大致浏览一下代码，对后面理解会好一些。关注微信公众号【zone7】后台回复【微服务】获取源码。
docker-compose
```
version: '2'
services:
  # consul server，对外暴露的ui接口为8500，只有在2台consul服务器的情况下集群才起作用
  consulserver:
    image: progrium/consul:latest
    hostname: consulserver
    ports:
      - "8300"
      - "8400"
      - "8500:8500"
      - "53"
    command: -server -ui-dir /ui -data-dir /tmp/consul --bootstrap-expect=2
    networks:
      - app

  # consul server1在consul server服务起来后，加入集群中
  consulserver1:
    image: progrium/consul:latest
    hostname: consulserver1
    depends_on:
      - "consulserver"
    ports:
      - "8300"
      - "8400"
      - "8500"
      - "53"
    command: -server -data-dir /tmp/consul -join consulserver
    networks:
      - app
  # consul server2在consul server服务起来后，加入集群中
  consulserver2:
    image: progrium/consul:latest
    hostname: consulserver2
    depends_on:
      - "consulserver"
    ports:
      - "8300"
      - "8400"
      - "8500"
      - "53"
    command: -server -data-dir /tmp/consul -join consulserver
    networks:
      - app
  # 监听容器中暴露的端口，一有新的端口，注册到注册中心
  registrator:
    image: gliderlabs/registrator:master
    hostname: registrator
    depends_on:
      - "consulserver"
    volumes:
      - "/var/run/docker.sock:/tmp/docker.sock"
    command: -internal consul://consulserver:8500
    networks:
      - app

# web 服务
  web-nodejs:
    build: ./webNodejs
    image: webapp:latest
    depends_on:
      - "consulserver"
    ports:
      - "3000"
    environment:
      SERVICE_3000_NAME: service-web
    networks:
      - app

# web 服务
  web-py:
    build: ./webPy
    image: webpy:latest
    ports:
      - "5000"
    environment:
      SERVICE_5000_NAME: service-web-py
    volumes:
      - ./webPy:/usr/local/work
    networks:
      - app
    command: bash -c "pip install -r requirements.txt && python app.py"

# api gateway
  gateway-py:
    build: ./gateWayPy
    image: gatewaypy:latest
    ports:
      - "5000:5000"
    environment:
      SERVICE_5000_NAME: service-gateway-py
    volumes:
      - ./gateWayPy:/usr/local/work
    networks:
      - app
    command: bash -c "pip install -r requirements.txt && python app.py"

# api gateway
  gateway-nodejs:
    build: ./gateWayJs
    image: gatewayjs:latest
    ports:
      - "3000:3000"
    environment:
      SERVICE_3000_NAME: service-gateway-js

    networks:
      - app

networks:
  app:
    driver: bridge
```

## registrator
关于 registrator ，上一篇文章已经有介绍，这里就不再赘述。这里找到一个中文文档，如下：
```
http://www.mamicode.com/info-detail-2383285.html#%E6%B3%A8%E5%86%8C%E5%90%8E%E7%AB%AF
```
下面简单介绍一下，docker-compose 中的命令：
```
command: -internal consul://consulserver:8500
连接到 consul 
```
```
environment:
      SERVICE_5000_NAME: service-web
设置服务发现中的名。
```
服务名是你在服务发现查找中使用的。缺省情况下，服务名按下面的格式确定：

<base(container-image)>[-<exposed-port> if >1 ports]

使用容器镜像的基础，如果镜像是 gliderlabs/footbar，服务名就是footbar。如果镜像是 redis,服务名就是简单的 redis。

而且如果一个容器有多个暴露端口，它将各自追加内部暴露端口以区别。例如，一个镜像 nginx 有两个暴露端口，80 和 443,将产生两个服务，分别命名 nginx-80 和 nginx-443。

你可以使用标签或者环境变量，SERVICE_NAME 或者 SERVICE_x_NAME，其中 x 是内部暴露端口，覆盖这些缺省名字。注意如果一个容器有多个暴露端口，设置SERVICE_NAME 会导致多个服务命名为 SERVICE_NAME-<exposed port>。
## API gateway
关于 API gateway，这里使用 nodejs 实现了一个简易版的 API gateway。说他简易，那真的事很简易，就只有服务发现和服务注册的功能。至于 python，也实现了一套，但是值得一提的事 python 的 consul 库不提供 服务监控功能，就是说当你新添加一个服务，程序是不会自动监控的。python 代码就不在贴出来了，详情请查看源码。
```
const Consul = require('consul');
const utils = require('./utils');
const serviceLocalStorage = require('./serviceLocalStorage.js');
class Discovery {
    connect(...args) {
        if (!this.consul) {
            console.log("与consul server连接中...")
            //建立连接，
            //需要注意的时，由于需要动态获取docker内的consul server的地址，
            //所以host需要配置为consulserver（来自docker-compose配置的consulserver）
            //发起请求时会经过docker内置的dns server，即可把consulserver替换为具体的consul 服务器 ip
            this.consul =new Consul({
                host:'consulserver',
                ...args,
                promisify: utils.fromCallback //转化为promise类型
            });
        }
        return this;


    }
    /**
     * 根据名称获取服务
     * @param {*} opts
     */
    async getService(opts) {
        if (!this.consul) {
            throw new Error('请先用connect方法进行连接');
        }
        const {service} = opts;
        // 从缓存中获取列表
        const services = serviceLocalStorage.getItem(service);
        if (services.length > 0) {
            console.log(`命中缓存，key:${service},value:${JSON.stringify(services)}`)
            return services;
        }
        //如果缓存不存在，则获取远程数据
        let result = await this
            .consul
            .catalog
            .service
            .nodes(opts);
        console.log(`获取服务端数据，key：${service}：value:${JSON.stringify(result[0])}  result: ${JSON.stringify(result)}`);
        serviceLocalStorage.setItem(service, result[0])
        return result[0];
    }
}

module.exports = new Discovery();
```
## web 服务
这里的 web 服务的主要功能就是获取当前主机的 ip 地址。我分别用 pyhon 和 nodejs 两种语言实现了一遍，其代码如下：
python 实现
```
app = Flask(__name__)
@app.route('/')
def a():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return "hello zone ！ip address ==> " + ip


@app.route('/index')
def index():
    c = consul.Consul(host='consulserver')
    (index, data) = c.catalog.service("service-web")
    host = str(data[0]["ServiceAddress"]) + ":" + str(data[0]["ServicePort"])
    print("==========="+host)
    r = requests.get('http://'+host)
    return r.text


if __name__ == '__main__':
    app.run(host='0.0.0.0')
#    app.run(host='0.0.0.0', debug=True)
```
nodejs 实现
```
const Application = require('koa');
const app = new Application();
const Router = require('koa-router');
const router = new Router();
const ip = require('ip');
router.get('/', async(ctx) => {
    ctx.body = {
    ip: ip.address()
}
})
//监听3000端口
app.listen(3000, () => {
    console.log('listen on port 3000')
});
app
    .use(router.routes())
    .use(router.allowedMethods);
```
## 运行
网页端访问：
![](https://upload-images.jianshu.io/upload_images/2470773-68d096a2a7f09a47.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
控制台 log，不断刷新网页边出现如下 bug：
![image.png](https://upload-images.jianshu.io/upload_images/2470773-fcceda9528876f57.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
现在关闭一个微服务：createnewinstance_web-py_1
服务发现监控信息如下：
![](https://upload-images.jianshu.io/upload_images/2470773-c4f17e441cf7f172.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


```
[{
	"Node": "consulserver",
	"Address": "172.22.0.3",
	"ServiceID": "registrator:dockermicroservices_web-py_2:5000",
	"ServiceName": "service-web",
	"ServiceTags": null,
	"ServiceAddress": "172.22.0.4",
	"ServicePortNode": "consulserver",
	"Address": "172.22.0.3",
	"ServiceID": "registrator:dockermicroservices_web-py_4:5000",
	"ServiceName": "service-web",
	"ServiceTags": null,
	"ServiceAddress": "172.22.0.6",
	"ServicePort": 5000
}, {
	"Node": "consulserver",
	"Address": "172.22.0.3",
	"ServiceID": "registrator:dockermicroservices_web-py_3:5000",
	"ServiceName": "service-web",
	"ServiceTags": null,
	"ServiceAddress": "172.22.0.5",
	"ServicePort": 5000
}]
```
新启动一个微服务：
```
version: '2'
services:
  web-py:
    build: ../webPy
    image: webpy:latest
#    depends_on:
#      - "consulserver"
    ports:
      - "5000"
    environment:
      SERVICE_5000_NAME: service-web
    volumes:
      - ../webPy:/usr/local/work
    networks:
      - app
    command: bash -c "pip install -r requirements.txt && python app.py"

networks:
  app:
    driver: bridge
```
运行命令 docker-compose up
监控服务：
```
[{
	"Node": "consulserver",
	"Address": "172.22.0.3",
	"ServiceID": "registrator:dockermicroservices_web-py_2:5000",
	"ServiceName": "service-web",
	"ServiceTags": null,
	"ServiceAddress": "172.22.0.4",
	"ServicePortNode": "consulserver",
	"Address": "172.22.0.3",
	"ServiceID": "registrator:dockermicroservices_web-py_4:5000",
	"ServiceName": "service-web",
	"ServiceTags": null,
	"ServiceAddress": "172.22.0.6",
	"ServicePort": 5000
}, {
	"Node": "consulserver",
	"Address": "172.22.0.3",
	"ServiceID": "registrator:dockermicroservices_web-py_3:5000",
	"ServiceName": "service-web",
	"ServiceTags": null,
	"ServiceAddress": "172.22.0.5",
	"ServicePort": 5000
}, {
	"Node": "consulserver",
	"Address": "172.22.0.3",
	"ServiceID": "registrator:createnewinstance_web-py_1:5000",
	"ServiceName": "service-web",
	"ServiceTags": null,
	"ServiceAddress": "172.25.0.2",
	"ServicePort": 5000
}]
```
多了一个微服务，说明服务发现成功。
## 后记
最重要的还是要自己去操作与实践，不然看懂了也没用。

参考文献：
[基于Docker实现服务治理（一）](https://zhuanlan.zhihu.com/p/36114437)
[基于Docker实现服务治理（二）](https://zhuanlan.zhihu.com/p/36471654)