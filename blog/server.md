## master服务器
```
[root@master ~]# docker ps -a
CONTAINER ID   IMAGE                 COMMAND                  CREATED         STATUS         PORTS                                                                      NAMES
e87c39052b53   mangomei/nginx:2.9    "/docker-entrypoint.…"   4 days ago      Up 4 days      0.0.0.0:80->80/tcp, :::80->80/tcp, 0.0.0.0:443->443/tcp, :::443->443/tcp   nginx
311321baacdf   snowdreamtech/frps    "/bin/sh -c '/usr/bi…"   12 months ago   Up 12 months                                                                              frps
4240951d114d   portainer/portainer   "/portainer"             16 months ago   Up 12 months   0.0.0.0:9000->9000/tcp, :::9000->9000/tcp                                  prtainer-test
```

## node服务器
```
docker volume create portainer_data
docker run -d --name portainer --restart=always -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
```

## hw服务器
* 安装portainer (已处理)
  

## 任务
* 将k8s(master,node)的集群停止掉，11月底master服务器将过期。（已处理）
* master服务器上的kiftd网盘需要迁移。
* 猫大刚主页恢复，将home-docsify从node服务器迁移到hw服务器(已处理)
* mb服务需要迁移 (已处理)
* card-api服务需要迁移，迁移到hw服务器（已处理）
* 生成卡片二维码的flask-api (已处理)
* card-api恢复 （已恢复）
* mb恢复 (已处理)
* 本地写作升级为远程服务器写作，统一跳板机。