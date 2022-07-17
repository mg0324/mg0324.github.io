---
title: "Java多线程同步控制方法"
date: 2022-07-17T16:44:52+08:00
draft: false
categories: ["Java并发"]
tags: ["java","juc"]
---

## 关键字Synchronized
关键字`Synchronized`、`Object.wat()`和`Object.notify()`是在jdk1.5之前用的多线程同步控制的方式，jdk1.5之后就提供了如下的`java.util.concurrent`工具包（简称为`juc`并发工具包），可以利用如下的新的工具来实现多线程间的同步。

如下代码，可以知道其使用场景及作用：
~~~
// 类T
class T {
    // 静态对象，是在类上的，只有一个
    private static Object lock = new Object();

    @SneakyThrows
    public void doSomething(){
        // 锁静态对象，只有一个，是系统一个锁
        synchronized (lock){
            lock.wait();
        }
    }
    public void doSomething2(){
        // 锁类对象，只有一个，是同一个锁
        synchronized (T.class){
           // 做一些事情
            lock.notify();
        }
    }
    // 修饰在实例方法上，实则是在调用对象上加锁，调用对象不同则锁不同
    public synchronized void doSomething3(){

    }

    // 修饰在静态方法上，实则是在当前类对象上加锁，只有一个锁
    public static synchronized void doSomething4(){

    }
}

~~~

## 重入锁 ReentrantLock
### 定义
重入锁可以允许一个线程连续2次获取同一把锁，当然解锁也需要解锁2次。(关键字synchronized也是重入锁）

### 重要方法
![](/mb/images/juc/sync/01.png)
* lock() 获取锁，如果锁被占用，则等待
* lockInterruptibly() 获取锁，但优先响应中断
可以利用中断来直接退出等待锁，释放资源，防止死锁
* tryLock() 尝试获取锁，理解返回结果；获取成功返回true，失败返回false
* tryLock(timeout,unit) 给定时间内尝试获取锁
* unlock() 释放锁

### 公平锁
构造方法内传递fair=true，则返回的是公平锁，默认是非公平锁，关键字synchronized也是非公平锁。
```
ReentrantLock lock = new ReentrantLock(true);
```
公平锁会按锁的线程等待队列的顺序，公平的让线程获取到锁，所以性能会比非公平锁低。

## 等待队列 Condition
`Condition`是重入锁的好搭档，让锁可以支持多个等待队列。提供了和`Object.wait()`、`Object.notify()`和对应功能的方法`Condition.await()`、`Condition.signal()`和`Condition.signalAll()`
![](/mb/images/juc/sync/02.png)

具体使用可参考`ArrayBlockQueue`的实现。

## 信号量 Semaphore
无论是内部锁synchronized还是重入锁ReentrantLock，一次都只允许一个线程访问临界区资源。而
`Semaphore`可以同时允许多个线程同时访问某一个资源。
构造方法如下：
~~~
public Semaphore(int permits)；// 第一个参数信号量数量
public Semaphore(int permits, boolean fair); // 第二个参数是否公平
~~~
主要方法如下：
```
public void acquire(); // 获取许可，阻塞直到获取到或者线程被中断
public void acquireUninterruptibly(); // 获取许可，阻塞直到获取到，不响应中断
public boolean tryAcquire(); // 尝试获取许可，直接返回结果
public boolean tryAcquire(long timeout,TimeUnit unit); // 在限定时间内尝试获取许可
public void release(); // 释放许可
```
是一个有效的流量控制工具，它基于AQS共享锁实现。常常用它来控制对有限资源的访问。
*   每次使用资源前，先申请一个信号量，如果资源数不够，就会阻塞等待；
*   每次释放资源后，就释放一个信号量。
 
## 读写锁 ReadWriteLock
读写分离锁可以减少锁竞争，提升性能，适合在读多写少的场景使用。
是JDK5中提供的，实现类有`ReentrantReadWriteLock`。
![](/mb/images/juc/sync/03.png)

~~~
ReadWriteLock readWriteLock = new ReentrantReadWriteLock();
Lock readLock = readWriteLock.readLock();// 读锁，共享锁
Lock writeLock = readWriteLock.writeLock();// 写锁，独占锁
~~~

## 倒计数器 CountDownLatch
CountDownLatch是一个非常实用的多线程控制工具类，可以让某一个线程等待，直到倒计数器结束。典型的场景，如火箭发射时的倒数计时（等待各个发射细节就位）。
![](/mb/images/juc/sync/04.png)
~~~
CountDownLatch countDownLatch = new CountDownLatch(3);
// 注意：相关检查是多线程并发执行的
// 检查1
// doCheck1()
countDownLatch.countDown();
// 检查2
// doCheck2()
countDownLatch.countDown();
// 检查3
// doCheck3()
countDownLatch.countDown();
// 等待检查完成，再执行发射逻辑
countDownLatch.await();
// 点火发射
// doFire()
~~~
## 循环栅栏 CyclicBarrier
`CyclicBarrier`也是一种多线程并发控制的工具，和`CountDownLatch`类似，前者可以重复使用，而后者只使用一次。
![](/mb/images/juc/sync/05.png)
例子：
~~~
public static void main(String[] args) {

    CyclicBarrier cyclicBarrier1 = new CyclicBarrier(2, () -> {
        System.out.println("满2个，group1执行完了");
    });
    CyclicBarrier cyclicBarrier2 = new CyclicBarrier(3, () -> {
        System.out.println("满3个，group2执行完了");
    });
    for(int i=0;i<100;i++) {
        boolean b = i % 2 == 0;
        Thread t1 = new Thread(() -> {
            try {
                if(b){
                    // 偶数，则到篱笆1
                    cyclicBarrier1.await();
                }else{
                    // 偶数，则到篱笆2
                    cyclicBarrier2.await();
                }

            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (BrokenBarrierException e) {
                e.printStackTrace();
            }
            System.out.println(Thread.currentThread().getName() + "跑完了");

        });
        t1.setName("t"+i);
        t1.start();
    }
}
~~~
输出：
```
满2个，group1执行完了
t2跑完了
t0跑完了
满3个，group2执行完了
t5跑完了
t1跑完了
t3跑完了
满2个，group1执行完了
t6跑完了
t4跑完了
满2个，group1执行完了
t10跑完了
t8跑完了
```
## 阻塞工具类 LockSupport
`LockSupport`是一个非常方便使用的线程阻塞工具，可以在任意线程内让线程阻塞，不需要先获得某个对象的锁，也不会抛出中断异常。（底层实现类似信号量_counter计数，当park时，这个变量置为了0，当unpark时，这个变量置为1）
 ~~~
LockSupport.park(); // 阻塞当前线程，也有限时等待，还支持中断响应
LockSupport.unpark(Thread.currentThread()); // 恢复某个线程
~~~

## 参考文档
* 书籍：葛一鸣 *《Java高并发程序设计第二版》


