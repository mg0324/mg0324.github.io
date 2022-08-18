---
title: "IDEA的启动速度优化"
date: 2022-08-18T22:40:42+08:00
draft: false
categories: ["技术文章","idea"]
tags: ["idea","jvm"]
---

## 前言
如果发现自己的IDE很慢，或者卡顿，那么就对它来一次调优吧。本人使用的是IDEA，如果是Eclipse的同学，可查找对应相关资料，本文仅供参考。

## 安装启动信息插件
笔者查找资料后，开发了IDEA启动信息的小插件，地址：https://gitee.com/mgang/idea-plugin-start-time 欢迎下载安装使用。

## 调优思路
* 选择IDEA合适的JDK版本，经过多种JDK尝试，使用默认`openjdk-11.0.6`，笔者IDEA版本信息如下：
```
IntelliJ IDEA 2019.3.5 (Community Edition)
Build #IC-193.7288.26, built on May 6, 2020
Runtime version: 11.0.6+8-b520.66 x86_64
VM: OpenJDK 64-Bit Server VM by JetBrains s.r.o
macOS 10.15.7
GC: G1 Young Generation, G1 Old Generation
Memory: 750M
Cores: 4
Registry: 
Non-Bundled Plugins: Lombook Plugin, PlantUML integration, PsiViewer, com.bruce.intellijplugin.generatesetter, com.damoguyansi.all-format, com.idlesign.qrcoder, com.mango.idea.plugin, jclasslib, leetcode-editor, ru.artyushov
```
如下是JDK尝试过的JDK版本：
![](/mb/images/idea/start-time/01.png) 
* 禁用类加载时的验证，减少时间 `-Xverify:none`
* 禁用系统调用GC，`-XX:+DisableExplicitGC`
* 可利用VisualVM或者JMC等可视化工具，查看IDEA的GC情况，将GC的停顿（STW）时间尽可能降低。根据自己机器内存，配置合适的JVM内存设置。
 `-Xms750m -Xmx750m -Xmn400m -XX:MetaspaceSize=248m -XX:MaxMetaspaceSize=500m`
![](/mb/images/idea/start-time/02.png) 
* 选择低延时的垃圾收集器，比如`-XX:+UseG1GC`

## 调优后JVM参数
经过调优后，本人IDEA的JVM参数如下：
~~~
-Xms750m
-Xmx750m
-Xmn400m
-XX:MetaspaceSize=248m
-XX:MaxMetaspaceSize=500m
-XX:+PrintGCDetails
-Xloggc://Users/mango/logs/ideagc.log
-verbose:gc
-Xverify:none
-XX:+DisableExplicitGC
-XX:+UnlockCommercialFeatures
-XX:+FlightRecorder
-XX:ReservedCodeCacheSize=240m
-XX:+UseG1GC
-XX:SoftRefLRUPolicyMSPerMB=50
-ea
-XX:CICompilerCount=2
-Dsun.io.useCanonPrefixCache=false
-Djava.net.preferIPv4Stack=true
-Djdk.http.auth.tunneling.disabledSchemes=""
-XX:+HeapDumpOnOutOfMemoryError
-XX:-OmitStackTraceInFastThrow
-Djdk.attach.allowAttachSelf=true
-Dkotlinx.coroutines.debug=off
-Djdk.module.illegalAccess.silent=true
-XX:+UseCompressedOops
-Dfile.encoding=UTF-8

-XX:ErrorFile=$USER_HOME/java_error_in_idea_%p.log
-XX:HeapDumpPath=$USER_HOME/java_error_in_idea.hprof
~~~
插件打印启动信息如下：
![](/mb/images/idea/start-time/03.png) 

