---
title: "Spring Cloud的注册中心"
date: 2022-01-19T23:29:48+08:00
categories: ["技术文章","Spring Cloud"]
tags: ["Spring Cloud","微服务"]
---

## 分布式系统CAP理论
![](/mb/images/sc/register/cap.png)
*   `Consistency 一致性`:所有数据备份，在同一时刻是否同样的值。（等同于所有节点访问同一份最新的数据副本）
*   `Availability 可用性`:在集群中一部分节点故障后，集群整体是否还能响应客户端的读写请求。（对数据更新具备高可用性）
*   `Partition Tolerance 容错性`:以实际效果而言，分区相当于对通信的时限要求。系统如果不能在时限内达成数据一致性，就意味着发生了分区的情况，必须就当前操作在C和A之间做出选择。

## Spring Cloud的4大注册中心
| 组件名称 | 实现语言 | CAP | 健康检查 |
| --- | --- | --- | --- |
| Eureka]| `Java` | AP | 可配 |
| Zookeeper | `Java` | CP | 支持 |
| Consul | `Golang` | CP | 支持 |
| Nacos | `Java` | AP | 支持 |

## 功能支持度比较
![](/mb/images/sc/register/vs.png)

## 参考文档
*   [注册中心ZooKeeper、Eureka、Consul 、Nacos对比](https://links.jianshu.com/go?to=https%3A%2F%2Fblog.csdn.net%2Ffly910905%2Farticle%2Fdetails%2F100023415)




