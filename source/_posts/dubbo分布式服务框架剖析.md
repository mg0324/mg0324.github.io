---
title: dubbo分布式服务框架剖析
date: 2017-04-27 17:15:25
categories: dubbo
tags:
- dubbo
- zookeeper
- redis
---

## Dubbo定位图
>首先，要知道dubbo是处于mvc中的model层，将传统的单应用分解成分布式服务的架构。
<div style="color:red;">
从而实现服务层的dubbo接口暴露和分布式带来的负载均衡好处。<br/>
顺便提一句，修改成分布式之后，请避免使用session这种单应用存储方式，不然会出现session的分布式共享问题。<br/>
一般都是使用单点登录，或者搭建redis集群来做分布式应用的公共存储空间。<br/>
</div>

<img src="/mb/images/dubbo-dw.png"/>

## Dubbo架构设计图
 
<img src="/mb/images/dubbo-jg.png"/>

## Dubbo注册中心

	其中的注册中心，有3种实现，zookeeper，redis，simple。

	其实注册中心是用来存储dubbo的提供者，消费者数据的，在提供者应用启动提供服务给注册中心时，
	就会写入数据到注册中心，在消费者调用服务时也会注册到注册中心会受到注册中心的服务通知列表，
	拿到可用的服务并且实现RPC。

	Dubbo官方采用的注册中心是zookeeper，因为zookeeper支持集群，分布式存储数据，能够搭建
	高可用的dubbo数据注册中心。

	而很多人不理解为什么redis也可以用来做dubbo的注册中心呢？redis不是一块nosql的key-value
	数据库服务么？其实，你仔细想想，dubbo的提供者，消费者的节点数据一样可以存储在redis中。
	Redis一样支持分布式存储和集群，所以也是可以做为dubbo的注册中心的。

<img src="/mb/images/dubbo-redis.png"/>

	dubbo使用zookeeper做注册中心，在zookeeper上的节点存储情况。
	使用的demo示例代码地址： 

<a href="http://git.oschina.net/mgang/dubbo-demo">http://git.oschina.net/mgang/dubbo-demo</a>

<img src="/mb/images/dubbo-zk.png" />

* Dubbo使用redis做注册中心，在redis中的存储情况。

<img src="/mb/images/dubbo-redis-zx.png" />





