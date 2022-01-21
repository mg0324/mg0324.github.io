---
title: "Spring Cloud初识"
date: 2022-01-16T19:27:32+08:00
draft: false
categories: ["技术文章","Spring Cloud"]
tags: ["Spring Cloud","微服务"]
---

## 微服务的出现
### 单体应用架构
从架构发展来看，单体应用架构存在很多问题：
* 复杂性高（项目包含多个模块，模块便捷不清，修改一个bug可能都会带来隐含的问题。）
* 技术债务（不坏不修）
* 部署评率低（全量部署耗时，出错概率高）
* 可靠性差（某个应用bug，例如死循环，`OOM`等，会导致整个应用崩溃）
* 扩展能力受限（无法按业务模块进行伸缩）
* 阻碍技术创新（例如一个使用`Struts2`的应用，已经写了100W行代码，想要切换成`springmvc`成本巨大。）
那么如何解决单体应用架构的问题呢？

### 什么是微服务架构
***微服务架构是一种将一个单一应用程序开发为一组小型服务的方法，每个服务运行在自己的进程中，服务间采用轻量级通信机制。服务可通过全自动部署机制独立部署，可用不同语言咖啡，使用不同的数据存储技术。***
微服务架构应具备的特性：
* 每个微服务可独立运行在自己的进程里。
* 一系列独立运行的微服务共同构建起整个系统。
* 每个服务为独立业务开发，一个微服务只关注某个特定的模块，例如订单管理，用户管理等。
* 微服务之前通过一些轻量的通信机制进行通信，例如`RESTful API`进行调用。
* 可以使用不同语言与数据存储技术。
* 全自动的部署机制。

微服务架构优点：
1. 易于开发和维护
2. 单个微服务启动快
3. 局部修改容易部署
4. 技术栈不受限
5. 按需伸缩

## 微服务框架
1. Spring Cloud - https://spring.io/projects/spring-cloud
2. Dubbo - https://dubbo.apache.org/zh/
3. Dropwizard - https://www.dropwizard.io/en/latest/
4. Armada - https://armada.sh/

***推荐Spring Cloud，具备开箱即用的生成特性，文档丰富，社区活跃，为微服务架构提供了完整的解决方案***

## Spring Cloud是什么
Spring Cloud是基于Spring Boot基础上构建的用于快速构建分布式系统的工具集。
具备如下特性：
1. 适应各种开发环境。
2. 隐藏组件复杂性。
3. 开箱即用，快速启动。
4. 轻量级组件。
5. 组件丰富，功能齐全。
6. 选型中立，丰富。
7. 灵活。

## Spring Cloud发展及版本
2015年3月发布Angel版本 1.0.0
![](/mb/images/sc/firstSee/01.png)

## Spring Cloud VS Dubbo
1. Dubbo只支持Java语言，Spring Cloud可集成Python，Nodejs等语言开发的微服务。
2. Dubbo通过RPC调用，Spring Cloud基于Http Restful调用，Dubbo占用带宽小。
3. Dubbo微服务组件功能不齐全，Spring Cloud个组件丰富。
Dubbo捐给Apache后，继续维护Dubbo3.x版本。
![](/mb/images/sc/firstSee/02.png)




