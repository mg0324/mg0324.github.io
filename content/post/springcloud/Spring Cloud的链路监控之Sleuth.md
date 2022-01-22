---
title: "Spring Cloud的链路监控之Sleuth"
date: 2022-01-22T12:25:00+08:00
draft: false
categories: ["技术文章","Spring Cloud"]
tags: ["Spring Cloud","微服务"]
---

## 前言
如果微服务调用出错了，如果快速定位问题呢？
`Spring Cloud`提供`Sleuth`来实现调用链监控。

## Sleuth基础概念
(1) Span（跨度）:
基本工作单元。span用一个64位的id唯一标识。除ID外，span还包含其他数据，例如描述、时间戳事件、键值对的注解（标签），span ID、span父ID等。
span被启动和停止时，记录了时间信息。初始化span被称为“root span”，该span的id和trace的id相等。
(2) Trace（跟踪）:
一组共享“root span”的span组成的树状结构称为trace。trace也用一个64位的ID唯一标识，trace中的所有span都共享该trace的ID。
(3) Annotation（标注）:
annotation用来记录事件的存在，其中，核心annotation用来定义请求的开始和结束。
![](/mb/images/sc/watch/01.png)
## 快速集成sleuth
1. 添加依赖
~~~
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-sleuth</artifactId>
</dependency>
~~~
2. 加配置
~~~
logging:
  level:
    com.github.mg0324.test.rpc: debug
    root: INFO
    org.springframework.cloud.sleuth: DEBUG
~~~
 其中，配置不是必选的，这里加上日志，只是为了看到更多Sleuth相关的日志。
3. 启动服务测试
![](/mb/images/sc/watch/02.png)
看到如上 `DEBUG [mic-test,1ba4e4c2ed20b601,a2803377608c1975,true] 1486` 这样的日志，就说明sleuth已经正常工作了。但是意义不大，还需要一个UI来做显示，这样才能更加直观地展示服务链路的监控。

