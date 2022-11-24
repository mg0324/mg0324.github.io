---
title: maven模块划分之部署深入
date: 2017-12-06 17:24:20
categories: ["技术文章","Java"]
tags: ["maven","部署方式","架构"]
draft: false
---

## 时机
> 在代码之路上快快慢慢几个春秋之后，多多少少都会经历一些框架的更迭。多数都是好用替代繁琐，新技术替换老技术。此刻，正是刚刚好的时机，来深入maven模块合理感谢华哥，受益匪浅的一课。

## 技术框架时间线
![技术时间线](http://osidurg5s.bkt.clouddn.com/skillTimeLine.png)
* jsp+servlet > 最原始无框架时期，会用一些dbutil,bootstartp等。
* ssh2+freemarker > struts2当时火，hibernate还未被mybatis攻克。
* ssm+freemarker > springmvc接手struts2，mybatis自定义sql轻量级。
* ssm+react > 前端框架泛滥，react组件化引入前端。
* sbm+react > springboot快速构建，代码精简。


## maven合理切分模块
![](http://osidurg5s.bkt.clouddn.com/mavenModuleCut.png)

## 部署方式
* 单系统网站级别部署方式
* 前后台分离无dubbo服务部署方式
* 前后台分离内部dubbo服务部署方式
* 前后台分离独立dubbo服务部署方式
![](http://osidurg5s.bkt.clouddn.com/fourDeployMethod.png)
> 能支持上面的部署方式，是因为maven模块的合理切分。




