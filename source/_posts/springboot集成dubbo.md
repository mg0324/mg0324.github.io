---
title: springboot集成dubbo
date: 2017-11-06 15:31:34
categories: springboot
tags:
- springboot
- dubbo
---

## pom.xml中加入springboot的dubbo启动依赖


	<dependency>
		<groupId>io.dubbo.springboot</groupId>
		<artifactId>spring-boot-starter-dubbo</artifactId>
		<version>1.0.0</version>
	</dependency>

## 加入dubbo的依赖接口jar包或者java文件
> 可以以jar包的方式引入，也可以用java文件来引入该`dubbo`的`interface`文件。

## 具体注入
> 该方式注入dubbo服务service，简单快捷。缺点：`@Reference`


	//@Reference(group = "bsp",timeout = 3000000)
    @Reference(group = "bsp",timeout = 300000000)
    private FormService formService;




