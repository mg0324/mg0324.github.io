---
title: 'java日志门面'
date: 2019-12-14 13:44:06
categories: java
tags:
- java
- slf4j
- logging
---



# 1.slf4j是什么

`slf4j`全称为`Simple Logging Facade for Java` ,即java简单日志门面，<font color=red>渐渐地替换调了`apache common logging`。</font>

> The Simple Logging Facade for Java (SLF4J) serves as a simple facade or abstraction for various logging frameworks (e.g. java.util.logging, logback, log4j) allowing the end user to plug in the desired logging framework at *deployment* time.

理解为是java应用程序里的日志门面或者是各种日志框架的抽象，其中常用的实现有`java.util.logging`,`logback`,`log4j`，目前主流的是`logback`。

<img src="/mb/images/slf4j/slf4j_framework.png" width="50%">

# 2.示例slf4j+logback

## 2.1.代码应用

![](/mb/images/slf4j/use.png)

级别依次是`trace`,`debug`,`info`,`warn`,`error`,越往下级别越高。

## 2.2.logback.xml配置

![](/mb/images/slf4j/logback.xml.png)

详细配置请参考 http://logback.qos.ch/manual/index.html