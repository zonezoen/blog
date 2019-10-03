- 瞎比比
- 什么都别说，先上图
- 需要什么配置条件？
- 如何配置？
- 关于 vscode 的插件
- 配置一个 python 开发环境
- 遇到的错误

## 瞎比比
最近看到 iPadOS 出来了，各种牛逼的操作真的很有吸引力，于是咬咬牙买了 iPad air。买来之后，当然是研究怎么提高效率了，于是就寻找、研究各种高效的软件。折腾了一段时间，各种 APP 都找得差不多了（有机会给大家分享一下），唯一的缺陷就是不能写代码。**一次偶然的机会，让我看到了一个 GitHub 项目：code-server，一个在浏览器中使用 vscode 编辑器的项目**。

## 什么都别说，先上图
![在笔记本 Chrome 浏览器上显示如图](https://upload-images.jianshu.io/upload_images/2470773-e245724d9fb821ee.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



![iPad Safari浏览器显示如图，并运行了 python 代码](https://upload-images.jianshu.io/upload_images/2470773-feadaefc7c281471.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Code-server 项目地址：[Github 地址](https://github.com/cdr/code-server)

怎么样，看图之后有没有很心动？不过这不是官方的项目，据说 5 月份的时候，官方也打算出一款网页的，但是至今没有什么消息。

## 需要什么配置条件？
- 一颗爱折腾的心
- 一台至少 1 核 2 g 的云服务器
- 一个可以访问网络的浏览器
- 需要有 docker 的基础知识
- 一个随时随地为公司加班的心 🤦‍♀️

## 如何配置？
我这篇文章是使用 docker 来搭建 vscode 的，如果你不懂 docker，可以查看我以前的 docker 入门文章，传送门：

如果你跟随官网的使用方法去搭建，那么恭喜你，踩坑了！就算搭建成功，并且能成功登陆页面，在你进行新建文件等各种操作的时候，他会提醒你，你没有权限完成该操作。
正确的使用方法应该是这样的：
```
docker run --user root -it -p "8080:8080" -v "/your/path/vscode/project:/home/coder/project" docker.io/codercom/codercom/code-server:v2  --allow-https --auth password
```
比官网的命令多一个：
```
—user root
```
是以 root 用户运行 docker 的意思，这样就不会出现没有权限问题了。
```
—auth password
```
是否加入登陆密码验证，如果没有加入的话，那么任何人都可以通过访问地址来访问你的编辑器了。

## 关于 vscode 的插件
在早一些的版本中，是无法在编辑器中直接安装插件的。**最新的版本好了一些，大部分插件都能直接搜索并且安装。**但是还是有少部分无法安装成功。这里提供一种离线安装的思路：
到网页版商店下载离线包，VSCode 扩展商店网页版：[https://marketplace.visualstudio.com/vscode](https://marketplace.visualstudio.com/vscode)
搜索扩展，进入到详情页之后，选择右下角的 Download Extension 下载离线包。
![](https://upload-images.jianshu.io/upload_images/2470773-cba70ee2b5c3478d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
之后在扩展界面选择Install from VSIX，选择路径安装。
![](https://upload-images.jianshu.io/upload_images/2470773-70b90c8e35f64060.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 配置一个 python 开发环境
code-server 正式版 V2 版本是无法成功配置 python 开发环境的，因为 V2 版本中无法在 vscode 中添加 python 配置。好在作者在试用版中 fix 了这个问题，其有效的版本如下：
```
docker run --user root -it -p "8080:8080" -v "/your/path/vscode/project:/home/coder/project" docker.io/codercom/code-server:2.1523-vsc1.38.1  --allow-https --auth password
```

然后在这个 docker 容器中安装 python3，打开 vscode debug 按钮下的命令行，输入如下命令：
![](https://upload-images.jianshu.io/upload_images/2470773-dd365a2cdaae9544.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
apt-get install python3
```
接下来，将 python3 重命名为 python：

```
cd /usr/bin
mv python3 python
```
然后在 vscode 中加载一个文件夹作为项目目录（/home/coder/project），如图：
![](https://upload-images.jianshu.io/upload_images/2470773-221d550fc41c9f3b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
由于我已经使用过了，所以也新建了几个 python 文件，
接下来，在 vscode 中，配置你的 python 环境，如图：
![](https://upload-images.jianshu.io/upload_images/2470773-9bdef330a6a5a735.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

配置完成之后，再在扩展库中找一些自己常用的工具库，那么就可以愉快的在浏览器中编辑 python 了。当然其他语言的也是差不多的操作。

## 遇到的错误
这里就罗列一下此次折腾中遇到的问题，如果你遇到问题解决不了，可以加我微信：
- 新建文件没有权限
- vscode 插件无法安装
- 配置好插件后，无法运行调试

