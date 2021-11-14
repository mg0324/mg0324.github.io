---
title: docker-machine的使用和总结
date: 2021-11-14 22:41:23
categories: 运维
tags: 
- docker
- docker-machine
- multipass
---

## 因子
最近在整理博客内容，因为平时使用`docker`的时候，见到了三剑客中的`docker-machine`，也就开始使用了。虽然现在`docker-machine`已经被官方弃用，不再维护更新，但是个人觉得其隔离性还是很好用的。（`Docker Desktop` 是官方主要更新维护的项目）

<img src="/mb/images/dm/01.png">
<!-- more -->

## 认识和基本使用
1. docker-machine 可以让你管理多个docker主机，能让你本地建立多个docker虚拟机，之前docker环境相互隔离。
2. 下载对应的二进制命令文件，加入到自己的命令库，就算是安装完成，删除则算是卸载完成。
3. 将docker-machine命令取别名dm，熟练使用ls、stop、start、ssh等命令。

<img src="/mb/images/dm/02.png">

4. 可以在自己的机器上安装多个docker-machine，一个做nginx的学习，一个做mysql的学习，相互之前不影响，然后利用vbox把端口上的服务映射出来。

## 例子：将dm内的p映射出来浏览器访问
1. 先创建一个test的隔离环境
``` bash
mango@mangodeMacBook-Pro ~ % dm create --driver virtualbox test
Running pre-create checks...
Creating machine...
(test) Copying /Users/mango/.docker/machine/cache/boot2docker.iso to /Users/mango/.docker/machine/machines/test/boot2docker.iso...
(test) Creating VirtualBox VM...
(test) Creating SSH key...
(test) Starting the VM...
(test) Check network to re-create if needed...
(test) Waiting for an IP...
Waiting for machine to be running, this may take a few minutes...
Detecting operating system of created instance...
Waiting for SSH to be available...
Detecting the provisioner...
Provisioning with boot2docker...
Copying certs to the local machine directory...
Copying certs to the remote machine...
Setting Docker configuration on the remote daemon...
Checking connection to Docker...
Docker is up and running!
To see how to connect your Docker Client to the Docker Engine running on this virtual machine, run: dm env test
```
2. ssh到test的docker machine上，运行portainer容器
``` bash
docker run -d -p 8000:8000 -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer\_data:/data portainer/portainer
```
``` bash
mango@mangodeMacBook-Pro ~ % dm ssh test
   ( '>')
  /) TC (\   Core is distributed with ABSOLUTELY NO WARRANTY.
 (/-_--_-\)           www.tinycorelinux.net

docker@test:~$ docker run -d -p 8000:8000 -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer\_data:/data portainer/portainer
Unable to find image 'portainer/portainer:latest' locally
latest: Pulling from portainer/portainer
94cfa856b2b1: Pull complete
49d59ee0881a: Pull complete
a2300fd28637: Pull complete
Digest: sha256:fb45b43738646048a0a0cc74fcee2865b69efde857e710126084ee5de9be0f3f
Status: Downloaded newer image for portainer/portainer:latest
aa130cadc27a40a24867f7cf54a76674e9457686bc4b6d30884f160908d29871
docker@test:~$ docker ps -a
CONTAINER ID        IMAGE                 COMMAND             CREATED             STATUS              PORTS                                            NAMES
aa130cadc27a        portainer/portainer   "/portainer"        6 seconds ago       Up 6 seconds        0.0.0.0:8000->8000/tcp, 0.0.0.0:9000->9000/tcp   portainer
```
3. 通过virtualbox的端口映射，将9000端口映射到宿主机
<img src="/mb/images/dm/03.png">

4. 通过浏览器访问代理的端口，http://127.0.0.1:10001
<img src="/mb/images/dm/04.png">
<img src="/mb/images/dm/05.png">

## docker-machine vs multipass
1. 面对的人员角度不同，`docker-machine`是面对`docker`容器环境的使用者，而`multipass`则是面对`ubuntu`操作系统环境的使用者。
2. 虽然都是借助虚拟机技术来得到VM环境，但范围体积不一样。
3. 都是通过建立不同虚拟机，来达到相互隔离的特性，通过网桥实现内部网络连通。
``` bash
mango@mangodeMacBook-Pro ~ % multipass ls
Name                    State             IPv4             Image
k3s                     Running           192.168.64.2     Ubuntu 20.04 LTS
                                          10.42.0.0
                                          10.42.0.1
node1                   Running           192.168.64.3     Ubuntu 20.04 LTS
                                          10.42.1.0
                                          10.42.1.1
rancher                 Running           192.168.64.4     Ubuntu 20.04 LTS
mango@mangodeMacBook-Pro ~ % multipass shell rancher
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-90-generic x86_64)
 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
  System information as of Sun Nov 14 22:26:19 CST 2021
  System load:  0.7               Processes:               115
  Usage of /:   27.6% of 4.67GB   Users logged in:         0
  Memory usage: 19%               IPv4 address for enp0s2: 192.168.64.4
  Swap usage:   0%
1 update can be applied immediately.
To see these additional updates run: apt list --upgradable
Last login: Sun Nov 14 22:25:51 2021 from 192.168.64.1
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.
ubuntu@rancher:~$
```


