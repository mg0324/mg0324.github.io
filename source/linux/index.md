---
title: linux专页
date: 2018-05-21 20:49:02
---

## linux释放内存
``` bash
echo 0 > /proc/sys/vm/drop_caches
```
这个文件中记录了缓存释放的参数，默认值为0，也就是不释放缓存。他的值可以为0~3之间的任意数字，代表着不同的含义：
* 0 – 不释放
* 1 – 释放页缓存
* 2 – 释放dentries和inodes
* 3 – 释放所有缓存

cache释放：说明，释放前最好`sync`一下，防止丢数据。
``` bash
sync
#去释放页内存:
echo 1 > /proc/sys/vm/drop_caches

#释放dentries and inodes内存:
echo 2 > /proc/sys/vm/drop_caches

#释放所有内存:
echo 3 > /proc/sys/vm/drop_caches
#释放之后记得free以下
free
```
## unbuntu防火墙问题，卡住docker 9998端口
首先`unbuntu`下的防火墙是`ufw`,`centos`下的是`service iptables`
``` bash
#unbuntu下开启防火墙
ufw enable
#unbuntu下关闭防火墙
ufw disable
#centos下开启防火墙
service iptables start
#centos下关闭防火墙
service iptables stop
```

## linux du命令
Linux du命令用于显示目录或文件的大小。du会显示指定的目录或文件所占用的磁盘空间。
``` bash
mango@mangodeMacBook-Pro mb % du -sh
309M
```

## oracle创建表空间
``` sql
#查询表空间位置
select file_name,tablespace_name,bytes from dba_data_files;
#创建表空间
create tablespace DV_DB_AR 
datafile 'T:\ORACLE\DV_DB_AR.DBF' 
size 2G  
autoextend on next 500M 
maxsize unlimited;
#创建临时表空间
create temporary tablespace DV_DB_AR_TEMP 
tempfile 'T:\ORACLE\DV_DB_AR_TEMP.DBF' 
size 2G 
autoextend on 
next 500M maxsize unlimited
extent management local;
```

## centos7安装ssh-copy-id命令，用于免密登陆
``` 
yum -y install openssh-clients
ssh-keygen
ssh-copy-id -i ~/.ssh/id_rsa.pub root@tw-master
```

## ss命令安装
``` 
yum install iproute -y // ss命令
```







