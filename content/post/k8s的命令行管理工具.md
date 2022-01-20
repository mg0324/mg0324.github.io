---
title: k8s的命令行管理工具
date: 2021-11-21 22:12:26
categories: ["技术文章"]
tags: ["k8s","云原生","kubectl","helm","k9s"]
draft: false
---

## 因子
k8s在2015年google开源之后，发展迅速，好多工具层出不穷。包括cmd工具和web端工具；本文主要关注cmd工具。

* kubectl - k8s command client
* helm - k8s yaml package util
* k9s - k8s plus client

## kubectl
可以使用 Kubectl 命令行工具管理 Kubernetes 集群，`kubectl`在`$HOME/.kube`目录中查找一个名为`config`的配置文件。可以通过设置 KUBECONFIG 环境变量或设置[`--kubeconfig`](https://kubernetes.io/zh/docs/concepts/configuration/organize-cluster-access-kubeconfig/)参数来指定其它[kubeconfig](https://kubernetes.io/zh/docs/concepts/configuration/organize-cluster-access-kubeconfig/)文件

详情请参考：https://kubernetes.io/zh/docs/reference/kubectl/overview/
### 示例
- 查看版本
``` bash
[root@master ~]# kubectl version
Client Version: version.Info{Major:"1", Minor:"21", GitVersion:"v1.21.1", GitCommit:"5e58841cce77d4bc13713ad2b91fa0d961e69192", GitTreeState:"clean", BuildDate:"2021-05-12T14:18:45Z", GoVersion:"go1.16.4", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"21", GitVersion:"v1.21.1", GitCommit:"5e58841cce77d4bc13713ad2b91fa0d961e69192", GitTreeState:"clean", BuildDate:"2021-05-12T14:12:29Z", GoVersion:"go1.16.4", Compiler:"gc", Platform:"linux/amd64"}
```
- 查看集群信息
``` bash
[root@master ~]# kubectl cluster-info
Kubernetes control plane is running at https://172.31.1.100:6443
CoreDNS is running at https://172.31.1.100:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```
- 查看集群节点
``` bash
[root@master ~]# kubectl get nodes
NAME  STATUS  ROLES AGE  VERSION
master  Ready control-plane,master  14d  v1.21.1
node1 Ready   14d  v1.21.1
```
``` bash
# 声明式创建资源
kubectl apply -f xxx.yaml
# 声明式删除资源
kubect delete -f xxx.yaml
# 获取所有命名空间下所有资源
kubect get all --all-namespaces
# 获取命名空间
kubectl get ns
# 查看pod日志
kubectl logs -f pod/xxx -n default
# 查看容器描述
kubectl describe pod/xxx -n default
```

## helm
官网网站：https://helm.sh/zh/
**Kubernetes** **包管理器** Helm 是查找、分享和使用软件构建[Kubernetes](https://kubernetes.io/)的最优方式。

Helm的一般操作：
*   helm search:   搜索chart
*   helm pull:    下载chart到本地目录查看
*   helm install:   上传chart到Kubernetes
*   helm list:     列出已发布的chart

详情请参考： https://helm.sh/zh/docs/helm/helm/
### 例子

![](/mb/images/k8s/helm-charts.png)

## k9s
k9s是一款k8s客户端管理工具，在kubectl基础上加强了命令行交互体验。
Kubernetes CLI 以时尚的方式管理您的集群！

![](/mb/images/k8s/k9s.png)

## 实际使用
通过 `--kubeconfig` 来指定配置文件。
``` bash
k9s --kubeconfig ~/.kube/k8s.yaml
```
![](/mb/images/k8s/k9s-ui.png)

