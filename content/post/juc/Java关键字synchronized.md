---
title: "Java关键字synchronized"
date: 2022-07-24T00:10:19+08:00
draft: false
categories: ["Java并发"]
tags: ["java","juc"]
---

## 提纲
![](/mb/images/juc/synchronized/01.png)

## 定义
`synchronized`是同步块，实现了多线程间的互斥同步。它修饰的代码，确保任一时刻只有一个线程进入访问。

## 特性
因为在`synchronized`同步块内，只有一个线程能访问，因此确保了同步块内的原子性、可见性和有序性。

## 使用方式
![](/mb/images/juc/synchronized/02.png)
总结：
```
Class tClass = T.class; // T.class其实就是该类的类对象
```
***synchronized不管是修饰代码块还是修饰方法，本质都是作用于对象上。进入代码块时需要获取对象锁，退出同步块是释放对象锁。***

## synchronized底层实现原理
![](/mb/images/juc/synchronized/03.png)
Java对象锁的信息存在Java对象头里的mark word中。  
synchronized不管是修饰代码块还是修饰方法，都能确定一个对象与之关联监视器。  
对象监视器(ObjectMonitor)是在jdk中使用c++实现的，具体细节需阅读对应源码。

## synchronized vs ReentrantLock
![](/mb/images/juc/synchronized/04.png)
总结：
1. 在`>=JDK1.6`后，`jvm`对`synchronized`关键字的锁做了很多优化，其性能和`ReentrantLock`的Api式锁相差无几；不过新的api的锁支持3个高级特性。
2. `ReentrantLock`的底层实现是基于`AQS`的；`synchronized`是`jvm`基于字节码`monitorenter`和`monitorexit`加上一些锁优化实现的。

## 提高锁性能
### 减少锁持有时间
![](/mb/images/juc/synchronized/05.png)
### 减小锁粒度
在`JDK1.7`中`ConcurrentHashMap`实用了分段锁来减小锁粒度（缩小锁对象的范围），从而降低锁冲突的可能性，进而提高系统的并发能力。
### 读写分离替换独占锁
在读多写少的场合使用读写锁可以有效提升系统的并发能力。
### 锁分离
锁分离是读写锁的进一步延伸，读写锁是根据读写操作上的不同，对锁进行了有效的分离。
在其他角度的分离思想，也可以对独占锁进行分离。
比如`LinkedBlockingQueue`的实现，其中`take()`和`put()`分别实现了从队列中获取数据和往队列中增加数据的功能，将独占锁分离为头锁和尾锁能提升`take()`和`put()`的并发能力。
![](/mb/images/juc/synchronized/06.png)

## 锁优化
在`<=JDK1.5`时，`synchronized`直接就是重量级锁，所以性能不好。在`JDK1.6`版本中，平台对这部分的锁性能做了很多优化，例如锁消除、锁粗化、偏向锁、自适应自旋、轻量级锁等优化。
### 锁消除
![](/mb/images/juc/synchronized/07.png)
低于JDK1.5版本，编译器会将+号连接字符串的代码优化为StringBuffer的连续append()操作；然后即时编译器会对代码做“逃逸分析”发现sb不会超出方法外，因此会将append方法内的同步完全消除掉执行，提高效率。
### 锁粗化
![](/mb/images/juc/synchronized/08.png)
虚拟机在遇到一连串连续地对同一个锁不断进行请求和释放的操作时，便会把所有的锁操作整合成对锁的一次请求，从而减少对锁的请求同步次数，这个操作叫做锁粗化。
### 偏向锁
优化思想：
如果一个线程获得了锁（通过CAS将当前线程指针记录到mark word中），那么锁就进入偏向模式，当该线程再次请求锁时，不需要做任何同步操作。

适用场景：
对于没有任何锁竞争的场合，偏向锁优化效果好。
***在锁竞争激烈的场景，如果每次来请求锁的线程都是不同线程，那么偏向模式会失效。***

JVM配置参数：
-XX:+UseBiasedLocking 开启偏向锁优化。
-XX:BiasedLockingStartupDelay=4 偏向锁延迟启动，默认4秒 。

### 轻量级锁
如果偏向锁失败，虚拟机会尝试轻量级锁的优化手段。

优化思想：
***对于绝大部分的锁，在整个同步周期内都是不存在竞争的。（这是一个经验数据）***

如果没有竞争，轻量级锁使用CAS操作避免使用互斥量的重量级锁开销。
单如果有竞争，CAS和互斥量开销都有，因此在有竞争的情况下，轻量级锁比重量级锁更慢。

实现：
在同步对象没有被锁定（锁标志位为01状态），虚拟机会在当前线程的栈中建立锁记录（Lock Record）的空间，然后通过CAS将对象的Mark Word对应位存储为锁记录的指针。如果成功，则说明获取轻量级锁成功，并更新该对象的Mark Word的锁标志位为00。

如果有2条以上线程争用同一个锁，则轻量级锁失效，会执行锁升级过程。

### 自旋&自适应自旋
如果轻量级锁失败，虚拟机还会做最后的尝试（自旋的优化）。

优化思想：
当前线程暂时无法获得锁，也许在几个CPU时钟周期后就可以获得锁。因此先不挂起线程，而是让线程做几个空循环后，如果获取到锁则进入临界区（还是轻量级锁状态）；如果还是没有获取到锁，就膨胀为重量级锁。

JVM配置参数：
-XX:+UseSpinning 开启自旋锁，JDK1.4.2已经引入，默认关闭。在JDK1.6之后默认开启。
-XX:PreBlockSpin=10 自旋次数，默认10次。后面加入自适应自旋后该参数无效。

自适应自旋：
手动设置自旋次数其实是不合理的，所以程序会根据前一次在同一个锁上的自旋时间及锁的拥有者状态来决定。
* 如果上一次刚刚成功通过自旋获取过锁，且持有锁的线程正在运行中，虚拟机会认为这次自旋也很有可能成功，进而允许更长时间的自旋等待。
* 如果对于某个锁，自旋很少成功过，则虚拟机会省略自旋获取锁的过程，避免浪费处理器资源。

## 锁升级
![](/mb/images/juc/synchronized/09.png)

详细流程如下图：
![](/mb/images/juc/synchronized/10.png)

例子：
~~~
/**
 * 锁升级测试 jdk版本=1.8
 * -XX:+UseBiasedLocking 默认1.6之后就开启了偏向锁
 * -XX:BiasedLockingStartupDelay=5  偏向锁启动延迟，单位秒，系统默认值是4
 *
 * 结论：
 *  当不开启偏向锁时，能得到 001（无锁） -> 000（轻量级锁） -> 010（重量级锁）
 *  开启偏向锁时，并设置延时5秒，new之后sleep 6秒，for循环内1个线程，则能得到 001(无锁） -> 000（轻量级锁） -> 101（偏向锁）
 *  开启偏向锁时，并设置延时5秒，new之后sleep 6秒，for循环内2个线程及以上，则能得到 001（无锁） -> 000（轻量级锁） -> 010（重量级锁）
 */
public class LockUpTest {
    // 锁对象
    private static Object lock = new Object();

    public static void main(String[] args) throws InterruptedException {

        // new状态 -- 001
        System.out.println(Thread.currentThread().getName() + " -- " + ClassLayout.parseInstance(lock).toPrintable());
        Thread.sleep(6000);

        synchronized (lock){
            // 轻量级锁 -- 000
            System.out.println(Thread.currentThread().getName() + " -- " + ClassLayout.parseInstance(lock).toPrintable());
        }

        // 偏向锁 -- 101
        Object newLock = new Object();
        new Thread(()->{
            synchronized (newLock) {
                System.out.println(Thread.currentThread().getName() + " -- " + ClassLayout.parseInstance(newLock).toPrintable());
            }
        }).start();

        // 重量级锁 -- 010（当线程数大于1）
        for(int i=0;i<2;i++){
            new Thread(()->{
                synchronized (lock) {
                    System.out.println(Thread.currentThread().getName() + " -- " + ClassLayout.parseInstance(lock).toPrintable());
                }
            }).start();
        }
    }
}
~~~
输出：
![](/mb/images/juc/synchronized/11.png)

## 参考资料
* 书籍 周志明 * 《深入理解Java虚拟机》
* 书籍 葛一鸣 * 《Java高并发程序设计》
* 网上文章 - https://www.cnblogs.com/Alei777/p/16223842.html


