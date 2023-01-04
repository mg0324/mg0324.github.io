---
title: "frp穿透你的远程桌面"
date: 2022-11-24T14:33:20+08:00
draft: false
categories: ["工具"]
tags: ["工具","frp","内网穿透","远程桌面"]
---
## 缘起

作为一个程序员，经常会遇到需要使用远程桌面的述求（居家办公、加班，你懂的）。所以，在网上找一圈远程桌面[解决方案](https://blog.csdn.net/mg0324/article/details/74182100?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166927427616782429766189%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=166927427616782429766189&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_ecpm_v1~rank_v31_ecpm-2-74182100-null-null.nonecase&utm_term=%E5%86%85%E7%BD%91&spm=1018.2226.3001.4450)之后，最终还是使用frp来穿透远程桌面。（推荐使用）

## 前提

* 需要一台有公网ip的服务器，腾讯云服务器或者阿里云服务器都可以
* 需要会docker的基本使用
* 知晓内网穿透[frp](https://github.com/fatedier/frp)的使用
* 针对windows系统的远程桌面配置

## 公网搭建frps服务端

本文服务端基于 `docker`安装 `frps`，镜像使用[snowdreamtech/frps](https://hub.docker.com/r/snowdreamtech/frps)。
详细配置请参考[frp文档](https://github.com/fatedier/frp/blob/dev/README_zh.md)。

配置文件frps.ini
```ini
# [common] is integral section
[common]
# A literal address or host name for IPv6 must be enclosed
# in square brackets, as in "[::1]:80", "[ipv6-host]:http" or "[ipv6-host%zone]:80"
bind_addr = 0.0.0.0
bind_port = 7000

# udp port to help make udp hole to penetrate nat
#bind_udp_port = 7001

# udp port used for kcp protocol, it can be same with 'bind_port'
# if not set, kcp is disabled in frps
#kcp_bind_port = 7000

# specify which address proxy will listen for, default value is same with bind_addr
# proxy_bind_addr = 127.0.0.1

# if you want to support virtual host, you must set the http port for listening (optional)
# Note: http port and https port can be same with bind_port
vhost_http_port = 81
#vhost_https_port = 443

# response header timeout(seconds) for vhost http server, default is 60s
# vhost_http_timeout = 60

# set dashboard_addr and dashboard_port to view dashboard of frps
# dashboard_addr's default value is same with bind_addr
# dashboard is available only if dashboard_port is set
dashboard_addr = 0.0.0.0
dashboard_port = 7500

# dashboard user and passwd for basic auth protect, if not set, both default value is admin
dashboard_user = admin
dashboard_pwd = a123456@

# dashboard assets directory(only for debug mode)
# assets_dir = ./static
# console or real logFile path like ./frps.log
log_file = ./frps.log

# trace, debug, info, warn, error
log_level = info

log_max_days = 3

# disable log colors when log_file is console, default is false
disable_log_color = false

# auth token
token = a123456@

# heartbeat configure, it's not recommended to modify the default value
# the default value of heartbeat_timeout is 90
# heartbeat_timeout = 90

# only allow frpc to bind ports you list, if you set nothing, there won't be any limit
#allow_ports = 2000-3000,3001,3003,4000-50000

# pool_count in each proxy will change to max_pool_count if they exceed the maximum value
max_pool_count = 5

# max ports can be used for each client, default value is 0 means no limit
max_ports_per_client = 0

# if subdomain_host is not empty, you can set subdomain when type is http or https in frpc's configure file
# when subdomain is test, the host used by routing is test.frps.com
#subdomain_host = meiflower.top

# if tcp stream multiplexing is used, default is true
tcp_mux = true

# custom 404 page for HTTP requests
# custom_404_page = /path/to/404.html
```
启动命令：
```shell
docker run --restart=always --network host -d -v /etc/frp/frps.ini:/etc/frp/frps.ini --name frps snowdreamtech/frps
```
启动成功后访问监控界面，`http://ip:7500`。
![](/mb/images/tool/frp-desktop/frps-admin.png)

## 本地windows电脑配置开启远程桌面
在我的电脑右键属性，进入远程桌面设置。

![](/mb/images/tool/frp-desktop/win-desktop.png)

给系统账号添加密码。

注意事项：
* 如果不想设置防火墙，建议将防火墙关掉，避免外网访问不到。
* 建议设置电源休眠选型，将电脑设置为永不休眠，笔记本盖上屏幕也不休眠。
* Windows的远程桌面端口默认为3389。
* 需要设置账号密码，无密码无法登录远程桌面。

## 本地安装frpc客户端并配置
### 下载frpc并启动
下载windows版本的fprc到本地,版本地址为https://github.com/fatedier/frp/releases

![](/mb/images/tool/frp-desktop/frpc-dir.png)

修改配置frpc.ini
``` ini
[common]
# 公网ip
server_addr = xxxx
server_port = 7000
token= a123456

[ssh]
type = tcp
local_ip = 127.0.0.1
local_port = 3389
remote_port = 9999
```
启动命令：
```
frpc.exe -c fprc.ini
```
### 设置frpc服务并开机自启
基于服务封装工作[nssm](https://blog.csdn.net/liyou123456789/article/details/123094277)，安装fprc为服务，并设置开机自启。

安装服务fprc:
``` shell
nssm install frpc
```

![](/mb/images/tool/frp-desktop/nssm-frpc.png)

安装成功后，继续设置服务frpc自启动。

![](/mb/images/tool/frp-desktop/service-enable-frpc.png)

如此Windows的远程桌面就成功在线了，且在电脑重启后会自动启动上线。如果电脑断电，也只需要联系同事帮忙打开电脑电源，就能成功远程。不需要像向日葵等软件掉线后还要一番操作，省心。

![](/mb/images/tool/frp-desktop/desktop-online.png)

## 得道
最后可以用远程桌面连接工具，远程到您的电脑，如此就能愉快的玩耍了。
优点：
* 连接稳定，图像清晰。
* 电脑重启后自动上线。
缺点：
* 需要公网IP
* 速度受公网ip带宽影响（建议将自己公网ip服务器的带宽调高一点，比如5M按量付费）
### 测试
* mac系统可以安装Microsoft Remote Desktop来连接windows的远程桌面。
* windows系统可用远程桌面连接工具：
![](/mb/images/tool/frp-desktop/do-connect.png)

* 安卓手机可以安装相应远程桌面连接软件，如下是手机连接测试图：
![](/mb/images/tool/frp-desktop/phone-connect.jpg)