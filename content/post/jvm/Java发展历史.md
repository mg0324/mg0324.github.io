---
title: "Java发展历史"
date: 2022-08-12T10:30:06+08:00
draft: false
categories: ["JVM"]
tags: ["java","jvm"]
---

## Java发展历史
![](/mb/images/jvm2/develop/01.png)
* 1995年5月23 Oak语言更名为Java
* 1996年1月23 JDK 1.0发布
* 1997年2月19日JDK 1.1发布
技术代表：JDBC，JAR文件格式，JavaBeans，RMI。
* 1998年12月4日里程碑版本 JDK1.2
 技术体系拆分为面向桌面级应用开发的J2SE、面向企业级应用开发的J2EE、面向手机等移动端开发的J2ME；这本版本的 Java虚拟机第一内置了JIT（编译器）。
* 1999年4月27HotSpot虚拟机发布
HotSpot最初是一家小公司开发，由于其优秀的 表现，这家公司在1997年被sun公司收购，HotSpot虚拟机发布时是作为Java1.2的附加程序提供的，后来它成为了JDK1.3以及之后的所有版本的Sun JDK的默认虚拟机。
* 2004年9月30日  JDK1.5发布
 工程代号Tiger，在语法易用性上做了很大的改进，例如：自动装箱，泛型，枚举，可变参数，遍历循环（foreach循环）等。
* 2006年11月13日 Sun公司宣布Java开源，建立OpenJDK组织对代码进行管理
* 2006年12月11日 JDK1.6发布
 启用Java SE6，Java 6EE，Java ME6的命名方式，提供动态语言支持，提供编译API，微型HTT服务器API；同时这个版本对Java虚拟机内部做了大量改进，包括锁与同步、垃圾收集、类加载等方面的算法都有很大的改动。
* 2009年12月，SUN公司发布Java EE 6
* 2011年7月28日，Oracle公司发布Java SE 7
* 2014年3月18日，Oracle公司发表Java SE 8(市场主流版本)
* 2017年9月21日，Oracle公司发表Java SE 9

后续版本待更新……
  
## Java体系结构
![](/mb/images/jvm2/develop/02.png)
主要包括Java虚拟机（JVM）、Java运行环境（JRE）以及一些工具（java、javac、javap等）共同构成Java开发套件（JDK）。

## 参考资料
* 周志明 * 《深入理解Java虚拟机》