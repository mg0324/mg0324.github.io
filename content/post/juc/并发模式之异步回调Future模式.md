---
title: "并发模式之异步回调Future模式"
date: 2022-07-28T10:42:57+08:00
draft: false
categories: ["Java并发"]
tags: ["java","juc"]
---

## Future模式（异步获取结果，自实现）
传统串行流程如下：
![](images/screenshot_1658934399592.png)
在获取数据时会阻塞等待，拿到数据后再执行其他的任务。
而`Future`模式会立即返回一个凭证（`Future`），这时可以执行其他任务；等需要数据再通过前面的`Future`凭证获取数据即可，流程如下图：
![](images/screenshot_1658934591907.png)

如下我们来自己实现一个简单的Future模式：
首先分析设计如下对象：
* Main 系统启动，调用Client发出请求，得到立即返回的FutureData
* Client 客户端，发出获取Data的请求，立即返回FutureData，并开启线程装配RealData
* Data 返回数据的接口
* FutureData 虚拟的数据，是一个凭证，需要装配RealData
* RealData 真实数据，构建较慢
代码如下：
Data接口：
~~~
public interface Data {
    String getResult() throws InterruptedException;
}
~~~
RealData类：
~~~
public class RealData implements Data{
    private String content;
    public RealData(String content){
        this.content = content;
    }
    @Override
    public String getResult() {
        return content;
    }
}
~~~
FutureData类：
~~~
public class FutureData implements Data {
    // 是否准备好
    private boolean isReady;
    // 组装真实数据
    private RealData realData;
    @Override
    public synchronized String getResult() {
        // 没有准备好，则阻塞等待
        while (!isReady){
            try {
                wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        return realData.getResult();
    }
    public synchronized void setRealData(RealData realData){
        if(isReady){
            return;
        }
        this.realData = realData;
        this.isReady = true;
        // 通知其他线程
        notifyAll();
    }
}
~~~
Client类：
~~~
public class Client {
    // 请求数据
    public FutureData request(String queryStr){
        FutureData futureData = new FutureData();
        // 开启线程异步出组装真实数据
        new Thread(()->{
            // 耗时操作
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            // 构建真实数据
            RealData realData = new RealData("hello future," + queryStr);
            futureData.setRealData(realData);
        }).start();
        // 立即返回
        return futureData;
    }
}
~~~
Main程序类：
~~~
public class Main {
    public static void main(String[] args) {
        Client client = new Client();
        FutureData futureData = client.request("测试");
        // 做其他的事情
        System.out.println("做其他事情1");
        System.out.println("做其他事情2");
        // 获取结果
        String result = futureData.getResult();
        System.out.println("异步结果为："+result);
    }
}
~~~
```
输出结果：
做其他事情1
做其他事情2
异步结果为：hello future,测试
```

## JDK中的Future模式
如下图，是`JDK1.8`中封装的`Future`模式实现。(1.5就又引入了`Future`模式，1.8的功能更加强大，提供了`CompletableFuture`)
![](images/screenshot_1658938711171.png)
其中：
* `类MyCallable`实现的`Callable`接口的`call()`方法会返回真实的数据（类似于自实现Future模式中的数据接口`Data`的`getResult()`方法)
* FutureTask类似于FutureData，都是用来当做异步调用里的立即返回的凭证
* 线程池类似于Client，都是用来执行任务的
如下是JDK的future的例子：
MyCallable类：
~~~
public class MyCallable implements Callable<String> {
    private String str;
    public MyCallable(String str){
        this.str = str;
    }
    @Override
    public String call() throws Exception {
        // 模拟比较耗时的操作
        Thread.sleep(2000);
        return "hello jdk future," + str;
    }
}
~~~
Main程序:
~~~
public class Main {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(1);
        FutureTask<String> futureTask = new FutureTask<>(new MyCallable("测试"));
        // 提交任务
        executor.submit(futureTask);
        System.out.println("处理其他逻辑1");
        System.out.println("处理其他逻辑2");
        String result = futureTask.get();
        System.out.println("(jdk)异步处理结果为:"+result);
        executor.shutdown();
    }
}
~~~
```
数据结果：
处理其他逻辑1
处理其他逻辑2
(jdk)异步处理结果为:hello jdk future,测试
```

另外，JDK的Future模式的Future接口还提供了一些高级的功能。
```
boolean cancel(boolean mayInterruptIfRunning);// 取消任务
boolean isCanclled();// 是否已经取消
boolean isDone();// 是否已经完成
V get(long timeout,TimeUnit unit);// 超时时间内获取结果
```

## Guava扩展Future模式
`JDK`的`Future`模式中，`future.get()`是阻塞的，不利于高并发开发。`Guava`增强了`Future`模式，增加了完成时的回调接口，使`future`完成时可以自动通知应用程序进行获取处理。

对上面的程序改造为guava的设置回调函数的方式，代码如下：
Main程序：
~~~
public class Main {
    public static void main(String[] args){
        ListeningExecutorService executorService = MoreExecutors.listeningDecorator(Executors.newFixedThreadPool(4));
        // 提交任务
        ListenableFuture<String> future = executorService.submit(new MyCallable("测试"));
        // 添加回调函数
        future.addListener(()->{
            String result = null;
            try {
                result = future.get();
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
            System.out.println("(guava)异步处理结果为:"+result);
        },MoreExecutors.directExecutor());
        System.out.println("处理其他逻辑1");
        System.out.println("处理其他逻辑2");
        executorService.shutdown();
    }
}
~~~
输出结果：
```
处理其他逻辑1
处理其他逻辑2
(guava)异步处理结果为:hello guava future,测试
```
## Netty扩展Future模式
netty中也提供了支持设置Future回调的扩展。
~~~
public class Main {
    public static void main(String[] args) {
        // 创建netty线程组
        EventExecutorGroup group = new DefaultEventExecutorGroup(4);
        // 提交任务
        Future<String> future = group.submit(new MyCallable("测试"));
        System.out.println("处理其他逻辑1");
        System.out.println("处理其他逻辑2");
        future.addListener(new FutureListener<String>(){
            @Override
            public void operationComplete(Future<String> future) throws Exception {
                String result = future.get();
                System.out.println("(netty)异步处理结果为:"+result);
            }
        });
        group.shutdownGracefully();
    }
}
~~~

## JDK8的CompletableFuture
`JDK8`中提供的`CompletableFuture`更加强大。
`CompletableFuture`实现了`CompletionStage`接口和`Future`接口，前者是对后者的一个扩展，增加了异步回调、流式处理、多个`Future`组合处理的能力，使`Java`在处理多任务的协同工作时更加顺畅便利。
使用`CompletableFuture`改造支持异步回调方法，代码如下：
MySupplier类：
~~~
public class MySupplier implements Supplier<String> {
    private String str;
    public MySupplier(String str){
        this.str = str;
    }

    @Override
    public String get() {
        // 模拟比较耗时的操作
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return "hello jdk CompletableFuture," + str;
    }
}
~~~
Main程序：
~~~
public class Main {
    public static void main(String[] args){
        CompletableFuture<String> future = CompletableFuture.supplyAsync(new MySupplier("测试"),
                Executors.newFixedThreadPool(1));
        future.whenCompleteAsync((r,t)->{
            System.out.println("(CompletableFuture)异步处理结果为:"+r);
        });
        System.out.println("处理其他逻辑1");
        System.out.println("处理其他逻辑2");
    }
}
~~~
输出结果：
```
处理其他逻辑1
处理其他逻辑2
(CompletableFuture)异步处理结果为:hello jdk CompletableFuture,测试
```

## 总结
1. 在`JDK1.5`中提供了`Future`模式，获取数据时阻塞的，所以其他框架（`guava`和`netty`)对`Future`模式做了扩展，支持了回调函数。
2. 在`JDK1.8`中提供了`CompletableFuture`，支持了更加强大的异步回调、流式处理、多个`Future`组合处理的能力。

## 参考资料
* 书籍 葛一鸣 * 《Java高并发程序设计》

