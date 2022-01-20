---
title: rancher的安装及使用
date: 2021-11-21 22:21:49
categories: ["技术文章"]
tags: ["k3s","rancher","云原生"]
draft: false
---

## rancher介绍
时至今日，Rancher已经成长为企业在生产环境中运行容器和Kubernetes的首要选择。  
同时也是为您提供跨任何基础设施部署Kubernetes即服务（Kubernetes-as–a-Service）的唯一选择。

备注：rancher是一家公司，同时也是其一款产品的名称，旗下还有k3s产品，longhorn等。

![](/mb/images/k8s/rancher-01.png)

## rancher安装
官方快速入门地址： https://www.rancher.cn/quick-start/
### 个人安装实践
在mac上使用mutlipass创建rancher的ubuntu vm做rancher安装。
``` bash
# 创建rancher vm，最好多给点磁盘空间，默认5G肯定是不够用的
multipass launch -n rancher -m 2G -d 20G
# 登录rancher
multipass shell rancher
# 安装docker(多种方式，这里使用青云命令行一键安装）
curl -sSL https://get.daocloud.io/docker | sh
# 以docker的host网络模式运行，如此rancher内部的local的k3s集群端口就能直接暴露到vm了
sudo docker run --privileged -d --restart=unless-stopped --name rancher --network=host -p 80:80 -p 443:443 rancher/rancher:v2.6-head
```
注意点：
1. `rancher`的环境矩阵要求，如果安装出错，可能是因为系统个软件环境不匹配导致。https://www.suse.com/suse-rancher/support-matrix/all-supported-versions/rancher-v2-6-2/
2. 以`docker`容器运行r`ancher`后，容器内会安装`k3s`集群的本地集群和`rancher`的UI管理界面。
3. 可以通过`docker logs -f rancher`查看容器启动日志，如果没有`exit error`等字样，等待片刻就能浏览器访问到rancher UI了。
## rancher使用
***安装的是rancher:v2.6-head版本***
1. 输入虚拟机IP访问，如 `https://192.168.64.4/`,

![](/mb/images/k8s/rancher-02.png)

2. 按照提示获取密码
``` bash
sudo docker logs rancher 2>&1 | grep "Bootstrap Password:"
2021/11/20 01:57:31 [INFO] Bootstrap Password:kxzhgnmdxkqnjx4j29trd7hmgjktcn482s6tf9pjhdl9qjqch8v6rx
```
3. 设置密码

![](/mb/images/k8s/rancher-03.png)

4. 设置中文，虽然各个版本界面布局有变化，但大同小异，摸索一下自然就会用了。

![](/mb/images/k8s/rancher-04.png)

5. 应用市场，集成了各种helm仓库，能快速安装主流k8s应用。

![](/mb/images/k8s/rancher-05.png)
