---
title: k3s初识及安装
categories: 运维
tags:
  - k3s
  - 云原生
abbrlink: 8a897575
date: 2021-11-21 22:20:33
---

2021-11-19 周5
## 介绍
[k3s](https://k3s.io/) 是轻量级 Kubernetes，专为物联网和边缘计算构建的经过认证的 Kubernetes 发行版。

<!-- more -->

架构图：

<img src="/mb/images/k8s/k3s.png">


## 优点
* 适合边缘计算
K3s 是一种高度可用、经过认证的 Kubernetes 发行版，专为无人值守、资源受限、远程位置或物联网设备内部的生产工作负载而设计。
* 简化和安全
K3s 打包为一个 <50MB 的二进制文件，可减少安装、运行和自动更新生产 Kubernetes 集群所需的依赖项和步骤。
* 针对 ARM 进行了优化
ARM64 和 ARMv7 都支持二进制文件和多架构映像。从 Raspberry Pi 到 AWS a1.4xlarge 32GiB 服务器，K3s 都能很好地工作。

## 快速开始
0. 一条命令安装server
``` bash
curl -sfL https://get.k3s.io | sh -
```
1. 下载 K3s -[最新版本](https://github.com/rancher/k3s/releases/latest)，支持 x86\_64、ARMv7 和 ARM64  
2. 运行服务器
``` bash
# 在master节点运行k3s服务器
sudo k3s server &
# k3s的Kubeconfig配置文件保存到/etc/rancher/k3s/k3s.yaml
sudo k3s kubectl get node

# 在不同的工作节点上运行agent服务 
# cat /var/lib/rancher/k3s/server/node-token 来查看token
sudo k3s agent --server https://myserver:6443 --token ${NODE_TOKEN}
```

## 利用multipass模拟安装
在`mac`上通过`multipass`来安装，[multipass](https://multipass.run/)能快速得到`Ubuntu VM`。
- 思路步骤
1. 先创建2个VM，一个master，一个node1。
2. 在master里安装k3s server。
3. 在node1里安装k3s agent。

## 实践
1. 创建k3s的VM
``` bash
mango@mangodeMacBook-Pro ~ % multipass launch --name k3s --mem 2G --disk 5G
Launched: k3s
```
2. 创建node1的VM
``` bash
mango@mangodeMacBook-Pro ~ % multipass launch --name node1 --mem 1G --disk 5G
Launched: node1
```
3. 进入k3s节点，安装k3s server
``` bash
# 进入k3s节点
multipass shell k3s
# 设置代理，如果没设置，下载k3s的文件会很慢，或者使用其他方式下载
ubuntu@k3s:~$ export https\_proxy=http://192.168.3.22:9999
# 一条命令安装k3s server
ubuntu@k3s:~$ curl -sfL https://get.k3s.io | sh -
[INFO] Finding release for channel stable
[INFO] Using v1.21.5+k3s2 as release
[INFO] Downloading hash https://github.com/k3s-io/k3s/releases/download/v1.21.5+k3s2/sha256sum-amd64.txt
[INFO] Downloading binary https://github.com/k3s-io/k3s/releases/download/v1.21.5+k3s2/k3s
[INFO] Verifying binary download
[INFO] Installing k3s to /usr/local/bin/k3s
[INFO] Skipping installation of SELinux RPM
[INFO] Creating /usr/local/bin/kubectl symlink to k3s
[INFO] Creating /usr/local/bin/crictl symlink to k3s
[INFO] Creating /usr/local/bin/ctr symlink to k3s
[INFO] Creating killall script /usr/local/bin/k3s-killall.sh
[INFO] Creating uninstall script /usr/local/bin/k3s-uninstall.sh
[INFO] env: Creating environment file /etc/systemd/system/k3s.service.env
[INFO]  systemd: Creating service file /etc/systemd/system/k3s.service
[INFO] systemd: Enabling k3s unit
Created symlink /etc/systemd/system/multi-user.target.wants/k3s.service → /etc/systemd/system/k3s.service.
[INFO] systemd: Starting k3s
```
4. 查看k3s集群节点和token
``` bash
ubuntu@k3s:$ sudo kubectl get nodes
NAME  STATUS  ROLES AGE VERSION
k3s Ready control-plane,master  6m9s  v1.21.5+k3s2
# 查看token，工作节点加入时需要使用
ubuntu@k3s:$ sudo cat /var/lib/rancher/k3s/server/node-token
K103588fd616ce143858b27ba24f10d0495d1f65d5427bda0f0083cb457dc191936::server:13e222641179e204ce76e2a57ca6af04
```
5. 进入node1节点，安装k3s agent工作节点
``` bash
# 进入node1节点
multipass shell node1
# 设置代理
export https_proxy=http://192.168.3.22:9999
# 并下载k3s命令
wget https://github.com/k3s-io/k3s/releases/download/v1.22.3%2Bk3s1/k3s
# 赋权
sudo chmod 777 k3s
# 将命令移动到 /usr/bin/ 下
sudo mv k3s /usr/bin/
```
``` bash
# node1节点上启动k3s agent，利用nohup & 后端运行
sudo nohup k3s agent --server https://192.168.64.2:6443 --token K103588fd616ce143858b27ba24f10d0495d1f65d5427bda0f0083cb457dc191936::server:13e222641179e204ce76e2a57ca6af04 &
```
6. 验证集群
``` bash
# k3s(master)节点上查看集群节点，能看到node1成功ready
ubuntu@k3s:$ sudo kubectl get nodes
NAME STATUS  ROLES AGE  VERSION
k3s  Ready control-plane,master  23m  v1.21.5+k3s2
node1  Ready   35s  v1.22.3+k3s1
```
至此，恭喜你已经通过`multipass`模拟安装`k3s cluster`成功。



