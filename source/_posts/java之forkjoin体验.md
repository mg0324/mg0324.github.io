---
title: java之forkjoin体验
date: 2020-03-06 10:52:37
categories: java
tags:
- forkjoin
- 并发编程
---

> 废话不多说，直接上代码！

```java
package org.mango.forkjoin;

import cn.hutool.http.HttpUtil;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.RecursiveTask;

public class ServiceTask extends RecursiveTask<String> {
    private String url;
    public ServiceTask(String url){
        this.url = url;
    }
    @Override
    protected String compute() {
        String result = HttpUtil.get(this.url);
        System.out.println(Thread.currentThread().getName()+"==>"+new Date().toLocaleString()+":"+result.substring(0,100));
        return result;
    }
    /**
     * 提交任务执行后返回结果
     * @return
     */
    public static List<String> execute(List<String> urls){
        List<String> resultList = new ArrayList<>();
        List<ServiceTask> subTasks = new ArrayList<ServiceTask>();
        for(String url : urls){
            ServiceTask subTask = new ServiceTask(url);
            subTasks.add(subTask);
            subTask.fork();
        }
        for(ServiceTask t : subTasks){
            resultList.add(t.join());
        }
        return resultList;
    }

    public static void main(String[] args) {
        List<String> urls = new ArrayList<>();
        for(int i=0;i<100;i++) {
            urls.add("http://mg.meiflower.top/card/rand");
        }
        long start = System.currentTimeMillis();
        List<String> resultList = ServiceTask.execute(urls);
        long end = System.currentTimeMillis();
        System.out.println("耗时"+(end-start)+"ms");
        /*for(String result : resultList){
            System.out.println(result.substring(0,100));
        }*/
    }
}
```

> 结果展示

```txt
ForkJoinPool.commonPool-worker-3==>2020-3-6 10:56:30:{"state":1,"msg":"","row":{"id":11,"v_key":"FastDFS","v_value":"FastDFS是一个开源的轻量级分布式文件系统，它对文件进行管理，功能包
ForkJoinPool.commonPool-worker-6==>2020-3-6 10:56:30:{"state":1,"msg":"","row":{"id":2,"v_key":"Vagrant","v_value":"Vagrant是一个基于Ruby的工具，用于创建和部署虚拟化开发环境。它 
ForkJoinPool.commonPool-worker-5==>2020-3-6 10:56:30:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
ForkJoinPool.commonPool-worker-1==>2020-3-6 10:56:30:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
ForkJoinPool.commonPool-worker-4==>2020-3-6 10:56:30:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
ForkJoinPool.commonPool-worker-7==>2020-3-6 10:56:30:{"state":1,"msg":"","row":{"id":4,"v_key":"辛辣","v_value":"辛辣是一个汉语词汇，读音为xīn là，是一种味道。意思是尖锐而强烈，此类食物包括葱
ForkJoinPool.commonPool-worker-2==>2020-3-6 10:56:30:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
ForkJoinPool.commonPool-worker-3==>2020-3-6 10:56:30:{"state":1,"msg":"","row":{"id":4,"v_key":"辛辣","v_value":"辛辣是一个汉语词汇，读音为xīn là，是一种味道。意思是尖锐而强烈，此类食物包括葱
ForkJoinPool.commonPool-worker-5==>2020-3-6 10:56:30:{"state":1,"msg":"","row":{"id":2,"v_key":"Vagrant","v_value":"Vagrant是一个基于Ruby的工具，用于创建和部署虚拟化开发环境。它 
ForkJoinPool.commonPool-worker-6==>2020-3-6 10:56:30:{"state":1,"msg":"","row":{"id":5,"v_key":"食品不耐受性","v_value":"食品不耐受性是对食物的一种不良反应，其不涉及免疫系统。反应的引起是由于不消化
耗时613ms
```

> 总结

1. forkjoin框架基于ForkJoinPool线程池线，不需用户管理线程。详情请跳转 https://www.cnblogs.com/cjsblog/p/9078341.html
2. 适用可拆分子任务的场景，比如计算1+2+3+……+100000的值。



下图参转载之 https://www.cnblogs.com/cjsblog/p/9078341.html

![](/mb/images/forkjoin.png)