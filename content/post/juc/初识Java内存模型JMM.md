---
title: "初识Java内存模型JMM"
date: 2022-07-06T11:22:04+08:00
draft: false
categories: ["Java并发"]
tags: ["java","juc"]
---

## 原子性、可见性、有序性

![](/mb/images/juc/jmm/01.png)

## 什么是指令重排，为什么需要？
要搞懂指令重排，首先要知道一条指令在CPU内是如何执行的，如下图约5个步骤。

![](/mb/images/juc/jmm/02.png)

为了加快指令并行速度，CPU硬件支持了流水线技术。

![](/mb/images/juc/jmm/03.png)

不同的指令步骤执行在不同的硬件局部，从而可以支持同时并发执行。

![](/mb/images/juc/jmm/04.png)

知道了CPU流水线之后，我们来看一个A=B+C的流水线执行过程例子：

![](/mb/images/juc/jmm/05.png)

如果按串行排列，则耗时4 * 5 = 20个时钟周期；使用CPU流水线并行技术后，可以只消耗9个时钟周期，节省了11个时钟周期的时间。所以流水线技术的引入，大大提高了CPU并行执行速度。
再看如下图的例子：

![](/mb/images/juc/jmm/06.png)

多条语句执行时，通过指令重排可以消除一些CPU中断，从而缩短执行时间，加快执行速度。

## 哪些指令不能重排：Happen-Before原则（先行发生）

![](/mb/images/juc/jmm/07.png)


