---
title: docker专页
date: 2018-01-30 17:59:27
---

* 1.docker 客户端临时连接远程docker服务器
> `export DOCKER_HOST="tcp://127.0.0.1:2375"` --  将IP更换为remote ip即可。

* 2.docker 容器和主机文件互相copy
> `docker cp 容器名:/opt/1.zip /opt` -- 将容器中的/opt/1.zip copy到主机/opt目录下。
 `docker cp /opt/tmp.zip 容器名:/opt` -- 将主机的/opt/tmp.zip文件copy到容器的/opt目录下。

* 3.docker 保存自己的容器为镜像
> `docker commit 容器名 mango/demo:1.0` -- 将容器提交为镜像，取名mango/demo,tag为1.0。

* 4.docker 导入导出镜像
> `docker export 容器名 > temp.tar` -- 将容器允许的镜像保存到temp.tar文件中
  `docker import temp.tar mango/temp:1.0` --从temp.tar中导入镜像，取名mango/temp,tag为1.0

* 5.给运行中的docker容器添加端口映射
> `iptables -t nat -A DOCKER -p tcp --dport 4900 -j DNAT --to-destination 	172.19.0.6:4900` 