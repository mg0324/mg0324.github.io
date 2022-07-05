---
title: "Java关键字volatile"
date: 2022-07-05T10:38:54+08:00
categories: ["Java并发"]
tags: ["java","juc"]
draft: false
---

# Java关键字volatile
## 提纲

![](/mb/images/juc/volatile/01.png)

## 定义
语义上，volatile是表示易变的、不确定的。
功能上，是Java提供的最轻量级的同步机制。

## 前因：从CPU缓存架构类比JMM线程工作内存和主内存关系
要弄懂如何保证可见性的，先要知道CPU的缓冲架构，如下图：

![](/mb/images/juc/volatile/02.png)

因为CPU的执行速度和内存的读写速度，相差太大。CPU完成操作后，如果要等到内存也执行完成再继续下一个操作的话，对CPU算力就是极大的浪费。所以为了匹配2者的速度差，引入了高速缓存。现在CPU一般都有3级缓存，其中一级缓存离CPU核最近，速度也最快，可分为指令缓存和数据缓存2部分；下面是二级缓存，一个CPU核心就配备一个一级缓存和二级缓存的，是私有的。而三级缓存则是共享的，再下面是数据总线和主内存。

如下图是CPU的基本信息：

![](/mb/images/juc/volatile/03.png)

引入了高速缓存，虽然能让CPU效率提升，但是也带来了缓存一致性问题。为了解决这个问题，引入了缓存一致性协议的解决方案，目前大多数采用的是MESI缓存一致性协议。（后续再详细讲解）

而对于Java并发环境下，多线程的共享数据一致性问题也是类似，Java内存模型参考上述的CPU缓存架构实现了自己的线程、工作内存和主内存的关系，如下图：

![](/mb/images/juc/volatile/04.png)

## 特性
因为Java内存模型对volatile关键字的支持，使得volatile修饰的变量（实例字段、静态变量或者数组对象的元素，不包含局部变量，因为局部变量是线程私有的）具备了如下特性：
* **多线程间的可见性**
* **有序性，禁止指令重排序**
* **不保证原子性，如volatile int i=1;i++；**

## volatile底层实现原理
### volatile修饰的底层区别
首先通过如下一段DCL（double check lock)程序来比对一下有volatile和没有volatile修饰变量的在汇编指令上的区别：
~~~
public class VolatileSingleton {
    public static volatile VolatileSingleton instance;
    public static VolatileSingleton getInstance(){
        if(instance == null){
            synchronized(VolatileSingleton.class){
                if(instance== null){
                    instance = new VolatileSingleton();
                }
            }
        }
        return instance;
    }
    public static void main(String[] args) {
        VolatileSingleton.getInstance();
    }
}
~~~
通过加上如下虚拟机参数，可以只显示getInstance()方法的汇编指令：
```
# server模式运行
-server 
# 让虚拟机编译模式执行代码
-Xcomp 
# 使用hsdis来显示执行的汇编指令，不同平台的hsdis插件请自行查阅安装
-XX:+UnlockDiagnosticVMOptions 
-XX:+PrintAssembly
# 如下2个命令，只打印关心部分的汇编指令，如果不指定会打印很多其他方法的汇编，造成混乱
# 编译命令，不要内联编译getInstance方法
-XX:CompileCommand=dontinline,*VolatileSingleton.getInstance 
# 编译命令，只编译getInstance方法
-XX:CompileCommand=compileonly,*VolatileSingleton.getInstance 
```
最后将没有加volatile修饰的汇编指令保存到novolatile.txt，加了volatile的保存到volatile.txt，再使用idea的compare with 对比如下图：

![](/mb/images/juc/volatile/05.png)

会发现加了volatile的会多出一行 **lock addl $0x0,(%rsp)** 的汇编指令，这个指令是一个内存屏障。
指令`lock addl $0x0,(%esp)`是一个空操作，关键在于 lock 前缀，查询 IA32 手册，它的作用是使得本 CPU 的 Cache 写入了内存，该写入动作也会引起别的 CPU invalidate 其 Cache。所以通过这样一个空操作，可让前面 volatile 变量的修改对其他 CPU 立即可见。

### volatile基于软内存屏障实现可见性和有序性

![](/mb/images/juc/volatile/06.png)

通过内存屏障指令lock，如果有修改，处理器会将该变量所在缓存行的数据会写到主内存，并使得其他CPU里该变量所在的缓存行失效，从而保证该变量的可见性。
而且内存屏障会保证后面的指令不会重排序到屏障前面，从而保证有序性。

可见性定义：对于共享变量a，当线程1修改a的值后，其他线程能立即知道这个修改，就说变量a对所有线程有可见性。
#### 可见性例子
~~~
/**
 * volatile 可见性测试
 */
public class VolatileVisibilityTest {
    private static volatile boolean ready;
    private static int number;

    private static class ReaderThread extends Thread{
        @Override
        public void run() {
            while (!ready);
            System.out.println(number);
        }
    }
    public static void main(String[] args) throws InterruptedException {
        new ReaderThread().start();
        Thread.sleep(1000);
        number = 42;
        ready = true;
        Thread.sleep(10000);
    }
}
/**
 * 因为JMM保证了volatile变量ready的可见性，在main线程中修改为true；
 * ReaderThread线程能应用到这个修改，则while(!ready)循环得以跳过。
 * 则输出42，,10秒后退出程序。如果ready没有修饰为volatile，则没有可见性，线程Reader会陷入死循环，程序永远不会停止。
 */
~~~

### volatile不保证原子性
比如复杂操作，i++;
~~~
/**
 * volatile不保证原子性
 * @Author: mango
 * @Date: 2022/7/4 11:32 下午
 */
public class VolatileNoAtomicTest {
    private static volatile int number = 0;

    static class AdderThread extends Thread{
        @Override
        public void run() {
            for(int i=0;i<10000;i++){
                number++;
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new AdderThread();
        t1.start();
        Thread t2 = new AdderThread();
        t2.start();
        t1.join();
        t2.join();
        System.out.println(number);
    }
}
/**
 * 结果：
 * 有时候输出小于20000的值，说明number++无法保证原子性
 */
~~~

## volatile优化
追加volatile变量的宽度为操作系统缓存行的宽度，一般为64字节。Java中对象的引用是4字节，`LinkedTransferQueue`会在每个入队元素的对象引用后填充60个字节，将元素补齐到64字节来提升并发下的入队和出队效率。使用追加到64字节的方式来填满高速缓冲区的缓存行，避免头接点和尾节点加载到同一个缓存行，使得头尾节点在修改时不会互相锁定。

### 不需要补齐到64字节的场景
1. 系统的缓存行不是64字节的，有的是32字节。
2. 共享变量不会被频繁的写。

## 参考资料
* 葛一鸣 * 《Java并发程序设计》
* 周志明 * 《深入理解Java虚拟机》
* 网上文章


