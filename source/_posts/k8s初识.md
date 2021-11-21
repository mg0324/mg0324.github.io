---
title: k8s初识
date: 2021-11-18 18:02:29
categories: 运维
tags: 
- k8s
- 云原生
---
2021-11-18 周4
## kubernetes是什么
kubernetes是一个google开源的容器编排平台，从创建应用，应用的部署，应用提供服务，扩容缩容应用，应用更新，都非常的方便，而且可以做到故障自愈，例如一个服务器挂了，可以自动将这个服务器上的服务调度到另外一个主机上进行运行，无需进行人工干涉。

<!-- more -->

### 架构图

<img src="/mb/images/k8s/struct.png">

### 特性（好处）
* 自动化容器的部署和复制
* 随时扩展或收缩容器规模
* 将容器组织成组（pod)，提供容器间的负载均衡
* 很容易地升级应用程序容器的新版本
* 提供容器弹性，如果容器失效就替换它


### 特性
<img src="/mb/images/k8s/future.png">

## kubernetes相关工具说明
* kubelet
* kubectl
* kubeadm
* minikube


## k8s集群的几种安装方式
* minikube 安装 - [交互式安装](https://kubernetes.io/zh/docs/tutorials/kubernetes-basics/create-cluster/cluster-interactive/)
* kubeadm安装 - 见文章 kubeadm安装k8s集群

<img src="/mb/images/k8s/method.png">

