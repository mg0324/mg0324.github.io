---
title: "Spring Cloud的链路监控之Zipkin"
date: 2022-01-22T12:26:36+08:00
draft: false
categories: ["技术文章","Spring Cloud"]
tags: ["Spring Cloud","微服务"]
---

## zipkin简介
Zipkin是Twitter开源的分布式跟踪系统，基于Dapper的论文设计而来。它的主要功能是收集系统的时序数据，从而追踪微服务架构的系统延时等问题。

官网：[http://zipkin.io/](http://zipkin.io/)

## ZipKin Server搭建
1.   使用[https://search.maven.org/remote\_content?g=io.zipkin.java&a=zipkin-server&v=LATEST&c=exec](https://search.maven.org/remote_content?g=io.zipkin.java&a=zipkin-server&v=LATEST&c=exec)下载最新版本的Zipkin Server，例如`zipkin-server-2.12.9-exec.jar`

2. 执行命令启动
`java -jar zipkin-server-2.12.9-exec.jar`

3.  访问`http://localhost:9411`即可看到Zipkin Server的首页。
![](/mb/images/sc/watch/03.png)

## 微服务集成ZipKin
1. 添加依赖
~~~
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-sleuth-zipkin</artifactId>
</dependency>
~~~
2. 添加配置
~~~
spring:
  zipkin:
    base-url: http://127.0.0.1:9411
  sleuth:
    sampler:
      # 采样率，模式0.1，也就是10%，为了便于观察效果，改为1.0，也就是100%。生产环境建议保持默认。
      probability: 1.0
~~~
3. 启动，并访问微服务，zipkin会记录到微服务调用链路
![](/mb/images/sc/watch/04.png)
![](/mb/images/sc/watch/5.png)




