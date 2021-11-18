---
title: k8s初识及kubeadm方式安装
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

## 安装前环境准备及说明
1. 服务器资源

|  机器   |  IP                   |    OS                                                        |    资源   |
| ------- | ----------------- | --------------------------------------------- | --------- |
| master | 172.31.1.100  |  CentOS Linux release 7.9.2009 (Core)   |  2C4G   |
| node1 | 172.30.1.100  |  CentOS Linux release 7.5.1804 (Core)   |  1C2G   |

***以上环境为个人学习环境，企业生产环境建议最低配置在8C16G master且master高可用，至少2台8C16G的工作节点***

2. 服务器环境准备
- 关闭防火墙和swap
``` bash
systemctl stop firewalld
setenforce 0
```
``` bash
# 临时关闭
swapoff -a    
# 永久关闭，注释掉swap配置行，重启reboot
vim /etc/fstab
```
- 网络相通
在服务器配置hosts，让机器间能通过主机名访问。
```
[root@node1 ~]# cat /etc/hosts
172.31.1.100 master
172.30.1.100 node1
```
```
[root@master ~]# ping node1
PING node1 (172.30.1.100) 56(84) bytes of data.
64 bytes from node1 (172.30.1.100): icmp_seq=1 ttl=64 time=1.72 ms
64 bytes from node1 (172.30.1.100): icmp_seq=2 ttl=64 time=1.66 ms
```
```
[root@node1 ~]# ping master
PING master (172.31.1.100) 56(84) bytes of data.
64 bytes from master (172.31.1.100): icmp_seq=1 ttl=64 time=1.72 ms
64 bytes from master (172.31.1.100): icmp_seq=2 ttl=64 time=1.69 ms
```
- 将桥接的IPV4流量传递到iptables 的链
``` bash
cat > /etc/sysctl.d/k8s.conf << EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sysctl --system
```

2. 安装容器环境docker
``` bash
# 获取阿里云的docker源
wget https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo -O/etc/yum.repos.d/docker-ce.repo
# yum 安装docker
yum -y install docker-ce
# 设置开机自启动
systemctl enable docker
systemctl start docker
# 查看docker版本
docker --version
Docker version 20.10.7, build f0df350
```

3. 安装kubelet环境，及工具kubectl和kubeadm
首先安装kubernetes环境，`kubelet`，然后安装命令行工具`kubectl`，再安装k8s集群安装工具`kubeadm`（还有其他的安装工具，如`minikube`等）
- 安装kubelet
先引入阿里云的kubernetes的repo
``` bash
cat > /etc/yum.repos.d/kubernetes.repo << EOF
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
```
然后执行安装命令（不指定版本会默认安装最新版本）
``` bash
yum install -y kubelet kubectl kubeadm
```
安装完成后，设置开机自启动 `kubelet`
``` bash
systemctl enable kubelet
```

## 开始安装k8s集群
### master节点安装
- 在master机器上使用`kubeadm init`初始化集群
其中使用阿里云的镜像仓库，不然下载镜像会很慢。
``` bash
kubeadm init --apiserver-advertise-address=172.31.1.100 --image-repository=registry.aliyuncs.com/google\_containers --pod-network-cidr=10.244.0.0/16 --kubernetes-version=v1.21.0
```
当出现如下输出，说明初始化成功！

<img src="/mb/images/k8s/kubeadm_init_1.png">

按要求执行第一个红框中的3条命令后，执行`kubectl get nodes`
```
[root@master ~]# kubectl get nodes
NAME     STATUS   ROLES                  AGE   VERSION
master   NotReady    control-plane,master   13d   v1.21.1
```
到这里master节点就部署完成了。（目前是单节点，master也能做集群，使其高可用）

**如果status是Not Ready，后面会安装网络组建，等几分钟就会变成Ready了**

### node1节点加入集群
- 在node1节点上使用`kubeadm join`命令加入k8s集群
``` bash
kubeadm join 172.31.1.100:6443 --token 4ex7v0.micj5oc8pd9ldnj8 \\  
\--discovery-token-ca-cert-hash sha256:57dd07de79741f66e29ae4371618ffa100e7dcc9272689a92708aef69ef1e157
```
如果出现如下输出，恭喜你node节点部署成功。
``` bash
This node has joined the cluster:  
Certificate signing request was sent to apiserver and a response was received.  
The Kubelet was informed of the new secure connection details.  
  
Run 'kubectl get nodes' on the control-plane to see this node join the cluster.
```

### 网络组件的安装
k8s内部资源间的通信，是通过自己的网络组件实现的。而k8s网络组建有多种实现，如`flannel`和`calico`等。（网络组件安装一种即可，推荐calico。）
- 安装calico网络组件
获取calico.yaml资源文件
```
wget https://docs.projectcalico.org/v3.10/getting-started/kubernetes/installation/hosted/kubernetes-datastore/calico-networking/1.7/calico.yaml
```
修改IP配置
``` bash
## 将192.168.0.0/16修改ip地址为10.244.0.0/16  
sed -i 's/192.168.0.0/10.244.0.0/g' calico.yaml
```
安装calico到k8s中
``` bash
kubectl apply -f calico.yaml
```
安装完成后，查看集群状态，都是Ready，到此k8s集群安装成功。
``` bash
[root@master ~]# kubectl get nodes
NAME     STATUS   ROLES                  AGE   VERSION
master   Ready    control-plane,master   13d   v1.21.1
node1    Ready    <none>                 13d   v1.21.1
```


