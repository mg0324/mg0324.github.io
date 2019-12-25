---
title: java之深入jvm之路
date: 2019-12-14 14:45:07
categories: java
tags:
- jdk
- jvm
- gc
- 垃圾回收
---
# 1.仔细看一看java
## 1.1.java发展历史
![](/mb/images/jvm/java-develop-time.png)
* 1995年5月23 Oak语言更名为Java
* 1996年1月23 JDK 1.0发布
* 1997年2月19日JDK 1.1发布
    > 技术代表：JDBC，JAR文件格式，JavaBeans，RMI。
* 1998年12月4日里程碑版本 JDK1.2
    > 技术体系拆分为面向桌面级应用开发的J2SE、面向企业级应用开发的J2EE、面向手机等移动端开发的J2ME；这本版本的 Java虚拟机第一内置了JIT（编译器）。
* 1999年4月27HotSpot虚拟机发布
    > HotSpot最初是一家小公司开发，由于其优秀的 表现，这家公司在1997年被sun公司收购，HotSpot虚拟机发布时是作为Java1.2的附加程序提供的，后来它成为了JDK1.3以及之后的所有版本的Sun JDK的默认虚拟机。
* 2004年9月30日  JDK1.5发布
    > 工程代号Tiger，在语法易用性上做了很大的改进，例如：自动装箱，泛型，枚举，可变参数，遍历循环（foreach循环）等。
* 2006年12月11日 JDK1.6发布
    > 启用Java SE6，Java 6EE，Java ME6的命名方式，提供动态语言支持，提供编译API，微型HTT服务器API；同时这个版本对Java虚拟机内部做了大量改进，包括锁与同步、垃圾收集、类加载等方面的算法都有很大的改动。
* 2006年11月13日 Sun公司宣布Java开源，建立OpenJDK组织对代码进行管理
* 2009年12月，SUN公司发布Java EE 6
* 2011年7月28日，Oracle公司发布Java SE 7
* 2014年3月18日，Oracle公司发表Java SE 8(市场主流版本)
* 2017年9月21日，Oracle公司发表Java SE 9

## 1.2.java体系结构
![](/mb/images/jvm/jdk-art.jpg)
# 2.仔细看一看jvm
## 2.1.jvm是什么
<img src="/mb/images/jvm/jvm-art.png" width="700px">

## 2.2.类加载（class loader）
### 2.2.1.类加载
当程序主动使用某个类时，如果该类还未被加载到内存中，则JVM会通过加载、连接、初始化3个步骤来对该类进行初始化。
![](/mb/images/jvm/class-load.jpeg)
（***加载 -> 链接（验证-准备-解析） -> 初始化 -> 使用 -> 卸载*** 等生命周期）
* 加载：
    > 加载指的是将类的class文件读入到内存，并为之创建一个java.lang.Class对象，也就是说，当程序中使用任何类时，系统都会为之建立一个java.lang.Class对象。
    类的加载由`类加载器`完成，`类加载器`通常由JVM提供，这些类加载器也是前面所有程序运行的基础，JVM提供的这些类加载器通常被称为系统类加载器。除此之外，开发者可以通过继承ClassLoader基类来创建自己的类加载器。
### 2.2.1.类加载器

## 2.3.运行时数据区（runtime data area)

### 2.3.1.方法区(method area)

### 2.3.2.jvm栈(jvm stack) & 本地方法栈(native method stack)

### 2.3.3.程序计数器(program counter register)

### 2.3.4.堆（heap）

## 2.4.执行子系统(execution engine) 


# 3.仔细看一看GC
## 3.1.什么是垃圾回收

## 3.2.如何定位垃圾

## 3.3.垃圾回收算法

## 3.4.JVM分代算法

## 3.5.常见的GC回收机制






# 5.JVM调优

# 7.如何查看jvm参数

