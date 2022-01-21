---
title: "SpringCloud的负载均衡之Ribbon"
date: 2022-01-21T22:45:53+08:00
draft: false
categories: ["技术文章","Spring Cloud"]
tags: ["Spring Cloud","微服务"]
---

## Ribbon介绍
Ribbon是Netfix发布的负载均衡器。
为Ribbon配置服务提供者地址后，基于负载均衡算法（内置轮询，随机等），自动帮消费者去请求。

## 集成Ribbon
注意本文使用的版本：
``` xml
<spring-cloud.version>Hoxton.SR10</spring-cloud.version>
<spring-boot-version>2.2.7.RELEASE</spring-boot-version>
```
前提是注册中心用的Eureka。
### 1.Eureka Client添加依赖
不用添加依赖，因为在eureka-client依赖里默认就集成了Ribbon。(你可以点进eureka-client的依赖内，找到如下依赖关系）
![](/mb/images/sc/slb/01.png)

### 2.为`RestTemplate`添加`@LoadBalanced`注解
``` java
@Bean
@LoadBalanced
public RestTemplate restTemplate() {
    return new RestTemplate();
}
```
### 3.Controller中使用`RestTemplate`请求微服务地址
``` java
@Autowired
private RestTemplate restTemplate;

@GetMapping("/cardRand")
public Result cardRand(){
    ResultObject<CardVo> result = (ResultObject<CardVo>) restTemplate.getForObject(
            "http://mic-card/card/admin/card/rand",
            ResultObject.class
    );
    return result;
}
```
### 4.验证
启动2个`mic-card`微服务的提供者，一边刷新浏览器请求，一边查看日志控制台输出。
能看到2个控制台均有日志输出，则说明微服务提供者已经有负载均衡了。

![](/mb/images/sc/slb/02.png)

## Ribbon提供的7中负载均衡策略
* com.netflix.loadbalancer.RoundRobinRule  - 轮询
* com.netflix.loadbalancer.RandomRule  - 随机
 * com.netflix.loadbalancer.RetryRule - 重试，先按RoundRobinRule进行轮询，如果失败就在指定时间内进行重试
 * com.netflix.loadbalancer.WeightedResponseTimeRule - 权重，响应速度越快，权重越大，越容易被选中。
 * com.netflix.loadbalancer.BestAvailableRule  - 先过滤掉不可用的处于断路器跳闸转态的服务，然后选择一个并发量最小的服务
 * com.netflix.loadbalancer.AvailabilityFilteringRule - 先过滤掉故障实例，再选择并发量较小的实例
 * com.netflix.loadbalancer.ZoneAvoidanceRule - 默认规则，复合判断server所在区域的性能和server的可用性进行服务的选择。

## 自定义Ribbon负债均衡策略
``` java
@Configuration
public class RibbonConfiguration {
    @Bean
    public IRule ribbonRule(){
        // 也可以自己做算法实现
        // return new RandomRule();
        return new RoundRobinRule();
    }
}
```

