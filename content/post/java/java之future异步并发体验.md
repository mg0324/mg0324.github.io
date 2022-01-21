---
title: java之future异步并发体验
date: 2020-03-06 11:36:48
categories: ["技术文章"]
tags: ["java","futrue","异步","并发编程"]
draft: false
---

> 废话不多说，直接上代码

``` java
package org.mango.demo;

import cn.hutool.http.HttpUtil;
import com.google.common.collect.Lists;
import com.google.common.util.concurrent.ListenableFuture;
import com.google.common.util.concurrent.ListeningExecutorService;
import com.google.common.util.concurrent.MoreExecutors;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.Executors;
import java.util.stream.Collectors;

public class FutrueCallableDemo {

    ListeningExecutorService guavaExecutor = MoreExecutors.listeningDecorator(Executors.newFixedThreadPool(8));
    List<ListenableFuture<String>> listListenableFuture = Lists.newArrayList();

    class ServiceTask implements Callable<String>{
        private String url;
        public ServiceTask(String url){
            this.url = url;
        }

        @Override
        public String call() throws Exception {
            String result = HttpUtil.get(this.url);
            System.out.println(Thread.currentThread().getName()+"==>"+new Date().toLocaleString()+":"+result.substring(0,100));
            return result;
        }
    }

    public List<String> execute(List<String> urls){
        for(String url : urls){
            ListenableFuture<String> future = guavaExecutor.submit(new ServiceTask(url));
            listListenableFuture.add(future);
        }
        long start = System.currentTimeMillis();
        List<String> resultList = listListenableFuture.stream().map(future -> {
            try {
                return future.get();
            } catch (Exception e) {
                e.printStackTrace();
                return null;
            }
        }).collect(Collectors.toList());
        long end = System.currentTimeMillis();
        System.out.println("耗时"+(end-start)+"ms");
        guavaExecutor.shutdown();//如果是局部线程池一定要关闭，不然线程池一直在跑，可能导致内存泄漏
        return resultList;
    }


    public static void main(String[] args) {
        FutrueCallableDemo futrueCallableDemo = new FutrueCallableDemo();
        List<String> urls = new ArrayList<>();
        for(int i=0;i<10;i++) {
            urls.add("http://mg.meiflower.top/card/rand");
        }
        List<String> resultList = futrueCallableDemo.execute(urls);
    }
}

```

> 输出结构

```txt
pool-1-thread-10==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-37==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":15,"v_key":"图灵测试","v_value":"图灵测试（The Turing test）由艾伦·麦席森·图灵发明，指测试者与
pool-1-thread-20==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":13,"v_key":"TreeSoft","v_value":"TreeSoft数据库管理系统，是使用java开发的，可以布署于win
pool-1-thread-22==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":5,"v_key":"食品不耐受性","v_value":"食品不耐受性是对食物的一种不良反应，其不涉及免疫系统。反应的引起是由于不消化
pool-1-thread-39==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":5,"v_key":"食品不耐受性","v_value":"食品不耐受性是对食物的一种不良反应，其不涉及免疫系统。反应的引起是由于不消化
pool-1-thread-31==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":13,"v_key":"TreeSoft","v_value":"TreeSoft数据库管理系统，是使用java开发的，可以布署于win
pool-1-thread-3==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":4,"v_key":"辛辣","v_value":"辛辣是一个汉语词汇，读音为xīn là，是一种味道。意思是尖锐而强烈，此类食物包括葱
pool-1-thread-12==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":5,"v_key":"食品不耐受性","v_value":"食品不耐受性是对食物的一种不良反应，其不涉及免疫系统。反应的引起是由于不消化
pool-1-thread-4==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":5,"v_key":"食品不耐受性","v_value":"食品不耐受性是对食物的一种不良反应，其不涉及免疫系统。反应的引起是由于不消化
pool-1-thread-33==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-7==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":4,"v_key":"辛辣","v_value":"辛辣是一个汉语词汇，读音为xīn là，是一种味道。意思是尖锐而强烈，此类食物包括葱
pool-1-thread-30==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-18==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":13,"v_key":"TreeSoft","v_value":"TreeSoft数据库管理系统，是使用java开发的，可以布署于win
pool-1-thread-27==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":13,"v_key":"TreeSoft","v_value":"TreeSoft数据库管理系统，是使用java开发的，可以布署于win
pool-1-thread-23==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":6,"v_key":"屠呦呦(youyou)先生","v_value":"1971年发现青蒿素治疗疟疾，2015年获得诺贝尔医学奖","
pool-1-thread-11==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-21==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-34==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":4,"v_key":"辛辣","v_value":"辛辣是一个汉语词汇，读音为xīn là，是一种味道。意思是尖锐而强烈，此类食物包括葱
pool-1-thread-13==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":6,"v_key":"屠呦呦(youyou)先生","v_value":"1971年发现青蒿素治疗疟疾，2015年获得诺贝尔医学奖","
pool-1-thread-2==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-15==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":6,"v_key":"屠呦呦(youyou)先生","v_value":"1971年发现青蒿素治疗疟疾，2015年获得诺贝尔医学奖","
pool-1-thread-24==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":3,"v_key":"Yarn","v_value":"Yarn是由Facebook、Google、Exponent 和 Tilde 联
pool-1-thread-28==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-26==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":6,"v_key":"屠呦呦(youyou)先生","v_value":"1971年发现青蒿素治疗疟疾，2015年获得诺贝尔医学奖","
pool-1-thread-16==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":2,"v_key":"Vagrant","v_value":"Vagrant是一个基于Ruby的工具，用于创建和部署虚拟化开发环境。它 
pool-1-thread-29==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":15,"v_key":"图灵测试","v_value":"图灵测试（The Turing test）由艾伦·麦席森·图灵发明，指测试者与
pool-1-thread-1==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":6,"v_key":"屠呦呦(youyou)先生","v_value":"1971年发现青蒿素治疗疟疾，2015年获得诺贝尔医学奖","
pool-1-thread-19==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":17,"v_key":"DDos","v_value":"分布式拒绝服务攻击可以使很多的计算机在同一时间遭受到攻击，使攻击的目标无法正常
pool-1-thread-40==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":3,"v_key":"Yarn","v_value":"Yarn是由Facebook、Google、Exponent 和 Tilde 联
pool-1-thread-8==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":6,"v_key":"屠呦呦(youyou)先生","v_value":"1971年发现青蒿素治疗疟疾，2015年获得诺贝尔医学奖","
pool-1-thread-36==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":15,"v_key":"图灵测试","v_value":"图灵测试（The Turing test）由艾伦·麦席森·图灵发明，指测试者与
pool-1-thread-35==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":6,"v_key":"屠呦呦(youyou)先生","v_value":"1971年发现青蒿素治疗疟疾，2015年获得诺贝尔医学奖","
pool-1-thread-17==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":5,"v_key":"食品不耐受性","v_value":"食品不耐受性是对食物的一种不良反应，其不涉及免疫系统。反应的引起是由于不消化
pool-1-thread-5==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":5,"v_key":"食品不耐受性","v_value":"食品不耐受性是对食物的一种不良反应，其不涉及免疫系统。反应的引起是由于不消化
pool-1-thread-38==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":19,"v_key":"lrzsz","v_value":"lrzsz是一款在linux里可代替ftp上传和下载的程序。","is_zf
pool-1-thread-14==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":3,"v_key":"Yarn","v_value":"Yarn是由Facebook、Google、Exponent 和 Tilde 联
pool-1-thread-6==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":15,"v_key":"图灵测试","v_value":"图灵测试（The Turing test）由艾伦·麦席森·图灵发明，指测试者与
pool-1-thread-25==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":16,"v_key":"LVS","v_value":"LVS是Linux Virtual Server的简写，意即Linux虚拟服务器
pool-1-thread-32==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":13,"v_key":"TreeSoft","v_value":"TreeSoft数据库管理系统，是使用java开发的，可以布署于win
pool-1-thread-9==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":4,"v_key":"辛辣","v_value":"辛辣是一个汉语词汇，读音为xīn là，是一种味道。意思是尖锐而强烈，此类食物包括葱
pool-1-thread-12==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":13,"v_key":"TreeSoft","v_value":"TreeSoft数据库管理系统，是使用java开发的，可以布署于win
pool-1-thread-23==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":11,"v_key":"FastDFS","v_value":"FastDFS是一个开源的轻量级分布式文件系统，它对文件进行管理，功能包
pool-1-thread-4==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":6,"v_key":"屠呦呦(youyou)先生","v_value":"1971年发现青蒿素治疗疟疾，2015年获得诺贝尔医学奖","
pool-1-thread-27==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":3,"v_key":"Yarn","v_value":"Yarn是由Facebook、Google、Exponent 和 Tilde 联
pool-1-thread-33==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":5,"v_key":"食品不耐受性","v_value":"食品不耐受性是对食物的一种不良反应，其不涉及免疫系统。反应的引起是由于不消化
pool-1-thread-30==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":3,"v_key":"Yarn","v_value":"Yarn是由Facebook、Google、Exponent 和 Tilde 联
pool-1-thread-26==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":13,"v_key":"TreeSoft","v_value":"TreeSoft数据库管理系统，是使用java开发的，可以布署于win
pool-1-thread-3==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":6,"v_key":"屠呦呦(youyou)先生","v_value":"1971年发现青蒿素治疗疟疾，2015年获得诺贝尔医学奖","
pool-1-thread-31==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":4,"v_key":"辛辣","v_value":"辛辣是一个汉语词汇，读音为xīn là，是一种味道。意思是尖锐而强烈，此类食物包括葱
pool-1-thread-18==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":11,"v_key":"FastDFS","v_value":"FastDFS是一个开源的轻量级分布式文件系统，它对文件进行管理，功能包
pool-1-thread-15==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":11,"v_key":"FastDFS","v_value":"FastDFS是一个开源的轻量级分布式文件系统，它对文件进行管理，功能包
pool-1-thread-21==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":6,"v_key":"屠呦呦(youyou)先生","v_value":"1971年发现青蒿素治疗疟疾，2015年获得诺贝尔医学奖","
pool-1-thread-19==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":6,"v_key":"屠呦呦(youyou)先生","v_value":"1971年发现青蒿素治疗疟疾，2015年获得诺贝尔医学奖","
pool-1-thread-20==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-36==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":16,"v_key":"LVS","v_value":"LVS是Linux Virtual Server的简写，意即Linux虚拟服务器
pool-1-thread-24==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":6,"v_key":"屠呦呦(youyou)先生","v_value":"1971年发现青蒿素治疗疟疾，2015年获得诺贝尔医学奖","
pool-1-thread-11==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":2,"v_key":"Vagrant","v_value":"Vagrant是一个基于Ruby的工具，用于创建和部署虚拟化开发环境。它 
pool-1-thread-22==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":16,"v_key":"LVS","v_value":"LVS是Linux Virtual Server的简写，意即Linux虚拟服务器
pool-1-thread-2==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-16==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":16,"v_key":"LVS","v_value":"LVS是Linux Virtual Server的简写，意即Linux虚拟服务器
pool-1-thread-29==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-13==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":3,"v_key":"Yarn","v_value":"Yarn是由Facebook、Google、Exponent 和 Tilde 联
pool-1-thread-8==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":15,"v_key":"图灵测试","v_value":"图灵测试（The Turing test）由艾伦·麦席森·图灵发明，指测试者与
pool-1-thread-39==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-34==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":13,"v_key":"TreeSoft","v_value":"TreeSoft数据库管理系统，是使用java开发的，可以布署于win
pool-1-thread-17==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":11,"v_key":"FastDFS","v_value":"FastDFS是一个开源的轻量级分布式文件系统，它对文件进行管理，功能包
pool-1-thread-37==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-5==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":6,"v_key":"屠呦呦(youyou)先生","v_value":"1971年发现青蒿素治疗疟疾，2015年获得诺贝尔医学奖","
pool-1-thread-14==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-28==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-1==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":11,"v_key":"FastDFS","v_value":"FastDFS是一个开源的轻量级分布式文件系统，它对文件进行管理，功能包
pool-1-thread-10==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":13,"v_key":"TreeSoft","v_value":"TreeSoft数据库管理系统，是使用java开发的，可以布署于win
pool-1-thread-7==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-25==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":17,"v_key":"DDos","v_value":"分布式拒绝服务攻击可以使很多的计算机在同一时间遭受到攻击，使攻击的目标无法正常
pool-1-thread-40==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":11,"v_key":"FastDFS","v_value":"FastDFS是一个开源的轻量级分布式文件系统，它对文件进行管理，功能包
pool-1-thread-32==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":17,"v_key":"DDos","v_value":"分布式拒绝服务攻击可以使很多的计算机在同一时间遭受到攻击，使攻击的目标无法正常
pool-1-thread-6==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":13,"v_key":"TreeSoft","v_value":"TreeSoft数据库管理系统，是使用java开发的，可以布署于win
pool-1-thread-35==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-38==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-9==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":11,"v_key":"FastDFS","v_value":"FastDFS是一个开源的轻量级分布式文件系统，它对文件进行管理，功能包
pool-1-thread-27==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":15,"v_key":"图灵测试","v_value":"图灵测试（The Turing test）由艾伦·麦席森·图灵发明，指测试者与
pool-1-thread-12==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":5,"v_key":"食品不耐受性","v_value":"食品不耐受性是对食物的一种不良反应，其不涉及免疫系统。反应的引起是由于不消化
pool-1-thread-4==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":3,"v_key":"Yarn","v_value":"Yarn是由Facebook、Google、Exponent 和 Tilde 联
pool-1-thread-23==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":4,"v_key":"辛辣","v_value":"辛辣是一个汉语词汇，读音为xīn là，是一种味道。意思是尖锐而强烈，此类食物包括葱
pool-1-thread-3==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":2,"v_key":"Vagrant","v_value":"Vagrant是一个基于Ruby的工具，用于创建和部署虚拟化开发环境。它 
pool-1-thread-26==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":5,"v_key":"食品不耐受性","v_value":"食品不耐受性是对食物的一种不良反应，其不涉及免疫系统。反应的引起是由于不消化
pool-1-thread-33==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":11,"v_key":"FastDFS","v_value":"FastDFS是一个开源的轻量级分布式文件系统，它对文件进行管理，功能包
pool-1-thread-18==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":13,"v_key":"TreeSoft","v_value":"TreeSoft数据库管理系统，是使用java开发的，可以布署于win
pool-1-thread-30==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":3,"v_key":"Yarn","v_value":"Yarn是由Facebook、Google、Exponent 和 Tilde 联
pool-1-thread-31==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":16,"v_key":"LVS","v_value":"LVS是Linux Virtual Server的简写，意即Linux虚拟服务器
pool-1-thread-16==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-21==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":13,"v_key":"TreeSoft","v_value":"TreeSoft数据库管理系统，是使用java开发的，可以布署于win
pool-1-thread-20==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":13,"v_key":"TreeSoft","v_value":"TreeSoft数据库管理系统，是使用java开发的，可以布署于win
pool-1-thread-2==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-22==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":6,"v_key":"屠呦呦(youyou)先生","v_value":"1971年发现青蒿素治疗疟疾，2015年获得诺贝尔医学奖","
pool-1-thread-36==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-24==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":11,"v_key":"FastDFS","v_value":"FastDFS是一个开源的轻量级分布式文件系统，它对文件进行管理，功能包
pool-1-thread-11==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":6,"v_key":"屠呦呦(youyou)先生","v_value":"1971年发现青蒿素治疗疟疾，2015年获得诺贝尔医学奖","
pool-1-thread-19==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":10,"v_key":"杨绛先生","v_value":"杨绛（1911年7月17日—2016年5月25日），本名杨季康， [1]  江
pool-1-thread-15==>2020-3-6 11:42:32:{"state":1,"msg":"","row":{"id":4,"v_key":"辛辣","v_value":"辛辣是一个汉语词汇，读音为xīn là，是一种味道。意思是尖锐而强烈，此类食物包括葱
耗时576ms

Process finished with exit code 0

```

> 总结

1. 线程池线程数最好是8的倍数，一般现在cpu都是8核心或者8的倍数。
2. 如果是使用的局部线程池，请使用完后记得关闭掉，避免内存泄漏。
3. 如果异步并发任务频繁，可以将局部线程池提升为全局，随应用启动创建，随应用退出销毁。