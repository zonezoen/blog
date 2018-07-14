# 基于 Docker 的 gitlab 搭建
# git-github-gitlab 
## git
git 是一款分布式版本控制软件，是由 Linux 的创造者 Linus 编写的。[更多关于 git 的介绍](http://blog.a0z.me/2014/05/21/GitBeginning/)
## github
github 是一个基于 git 的 web 协作社区，它有多种机制让大家协同的和你一起的对项目进行贡献。它允许你自由创建共有仓库，但是私有仓库需要付费。值得关注的事，最近 github 被微软收购了。其实 github 发展到现在，已经拥有了更多的属性了，例如：

 1. 有简历的属性，当你面试一家公司的时候，可以列出自己的 github 地址，这是面试中的一个加分项。
 2. 可以利用 github 搭建自己的博客。
 3. 与别人共同完成一个项目。
 4. github 可以作为自己的简历，例如：[戳这里](https://github.com/hit9/GhResume)

## gitlab
gitlab 和 github 差不多，都是提供远程访问 git 存储库的服务。方便控制你的源代码版本。但是 gitlab 可以自由创建公有的和私有的代码仓库。
# gitlab yml 代码
```
version: '2'
services:
  gitlab:
    image: 'gitlab/gitlab-ce:latest'
    restart: always
    hostname: 'test.***.com'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://test.***.com'
    ports:
      - '30080:80'
      - '30443:443'
      - '30022:22'
    volumes:
      - './gitlab/config:/etc/gitlab'
      - './gitlab/logs:/var/log/gitlab'
      - './gitlab/data:/var/opt/gitlab'
```
值得注意的是，external_url 为外部访问地址。