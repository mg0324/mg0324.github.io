---
title: "Spring Cloud的熔断器"
date: 2022-01-21T23:12:22+08:00
draft: false
categories: ["技术文章","Spring Cloud"]
tags: ["Spring Cloud","微服务"]
---

## 熔断器介绍
### 为什么需要熔断器
当一个调用，里面跟着调用其他微服务时，其他微服务不可用，就会阻塞调用线程，从而可能导致调用链路前的微服务不可用，最终导致雪崩。（雪崩效应）

![](/mb/images/sc/rdq/01.png)

这个时候就需要有熔断机制作为保护。

### 熔断器三板斧
* 超时机制
* 舱壁模式
* 断路器

![](/mb/images/sc/rdq/02.png)

## 支持的熔断器
目前Spring Cloud生态中，支持的断路器有：Hystrix、Resilience4J、Alibaba Sentinel，虽然彼此实现有较大差异，但本质原理是相通的。

![](/mb/images/sc/rdq/03.png)

## 参考
* https://www.itmuch.com/spring-cloud/finchley-12/