---
title: linux专页
date: 2018-05-21 20:49:02
---

## 一.linux释放内存
> `echo 0 > /proc/sys/vm/drop_caches`
> 这个文件中记录了缓存释放的参数，默认值为0，也就是不释放缓存。他的值可以为0~3之间的任意数字，代表着不同的含义：
* 0 – 不释放
* 1 – 释放页缓存
* 2 – 释放dentries和inodes
* 3 – 释放所有缓存

> cache释放：说明，释放前最好`sync`一下，防止丢数据。


	sync
	#去释放页内存:
	echo 1 > /proc/sys/vm/drop_caches
	
	#释放dentries and inodes内存:
	echo 2 > /proc/sys/vm/drop_caches
	
	#释放所有内存:
	echo 3 > /proc/sys/vm/drop_caches
	#释放之后记得free以下
	free

## 二.`unbuntu`防火墙问题，卡住`docker 9998`端口
> 首先`unbuntu`下的防火墙是`ufw`,`centos`下的是`service iptables`


	#unbuntu下开启防火墙
	ufw enable
	#unbuntu下关闭防火墙
	ufw disable


	#centos下开启防火墙
	service iptables start
	#centos下关闭防火墙
	service iptables stop








