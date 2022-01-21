---
title: "Spring Cloud的熔断器监控"
date: 2022-01-21T23:19:48+08:00
draft: false
categories: ["技术文章","Spring Cloud"]
tags: ["Spring Cloud","微服务"]
---

## Hystrix监控
### actuator的监控节点
在`actuator`下有用来监控`hystrix`的端点`/actuator/hystrix.stream`。

访问：
```
http://localhost:9202/actuator/hystrix.stream
```
输出：(注意监控时需要请求`@HystrixCommand`配置的微服务)
```
ping: 

data: {"type":"HystrixCommand","name":"feignCardRand","group":"TestController","currentTime":1641272819332,"isCircuitBreakerOpen":false,"errorPercentage":0,"errorCount":0,"requestCount":1000,"rollingCountBadRequests":0,"rollingCountCollapsedRequests":0,"rollingCountEmit":0,"rollingCountExceptionsThrown":0,"rollingCountFailure":0,"rollingCountFallbackEmit":0,"rollingCountFallbackFailure":0,"rollingCountFallbackMissing":0,"rollingCountFallbackRejection":0,"rollingCountFallbackSuccess":0,"rollingCountResponsesFromCache":0,"rollingCountSemaphoreRejected":0,"rollingCountShortCircuited":0,"rollingCountSuccess":1000,"rollingCountThreadPoolRejected":0,"rollingCountTimeout":0,"currentConcurrentExecutionCount":0,"rollingMaxConcurrentExecutionCount":10,"latencyExecute_mean":0,"latencyExecute":{"0":0,"25":0,"50":0,"75":0,"90":0,"95":0,"99":0,"99.5":0,"100":0},"latencyTotal_mean":0,"latencyTotal":{"0":0,"25":0,"50":0,"75":0,"90":0,"95":0,"99":0,"99.5":0,"100":0},"propertyValue_circuitBreakerRequestVolumeThreshold":20,"propertyValue_circuitBreakerSleepWindowInMilliseconds":5000,"propertyValue_circuitBreakerErrorThresholdPercentage":50,"propertyValue_circuitBreakerForceOpen":false,"propertyValue_circuitBreakerForceClosed":false,"propertyValue_circuitBreakerEnabled":true,"propertyValue_executionIsolationStrategy":"THREAD","propertyValue_executionIsolationThreadTimeoutInMilliseconds":1000,"propertyValue_executionTimeoutInMilliseconds":1000,"propertyValue_executionIsolationThreadInterruptOnTimeout":true,"propertyValue_executionIsolationThreadPoolKeyOverride":null,"propertyValue_executionIsolationSemaphoreMaxConcurrentRequests":10,"propertyValue_fallbackIsolationSemaphoreMaxConcurrentRequests":10,"propertyValue_metricsRollingStatisticalWindowInMilliseconds":10000,"propertyValue_requestCacheEnabled":true,"propertyValue_requestLogEnabled":true,"reportingHosts":1,"threadPool":"TestController"}
```

### 集成hystrix dashboard
接口数据查看起来不直观，可以运行`hystrix dashboard`通过界面来查看。
1. 先引入依赖
~~~ xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-hystrix-dashboard</artifactId>
</dependency>
~~~
2. 创建启动类
~~~ java
@EnableHystrixDashboard
@SpringBootApplication(scanBasePackages = "com.github.mg0324")
public class StartupApplication {
    public static void main(String[] args) {
        SpringApplication.run(StartupApplication.class,args);
    }
}
~~~
3. 添加首页跳转，支持端口直接到`hystrix`资源路径
~~~ java
@Controller
public class HystrixIndexController {
  @GetMapping("")
  public String index() {
    return "forward:/hystrix";
  }
}
~~~
4. 添加配置端口
~~~
server:
  port: 8030

hystrix:
  dashboard:
    # 设置允许连接的IP
    proxy-stream-allow-list: "192.168.3.29"
~~~
5. 启动服务，并访问 `http://127.0.0.0:8030`
![](/mb/images/sc/rdq/dashboard.png)

### 监控详情解读
在 Hystrix Dashboard 界面里的url处填写要监控的hystrix数据流地址。
如：http://192.168.3.29:9202/actuator/hystrix.stream

![](/mb/images/sc/rdq/dashboard01.png)

如果连接后的界面里什么都没有显示，则需要手动请求后，才能展现数据。可以用 ab 命令做请求压测，加大压力，让熔断器开启，图中会出现红色。

![](/mb/images/sc/rdq/dashboard02.png)


ab命令如下：
`ab -n 10000 -c 160 http://127.0.0.1:9201/test/test/feign/cardRand`

![](/mb/images/sc/rdq/ab.png)

## 集成Turbine监控
Turbine是一个聚合Hystrix监控数据的工具，它可将所有相关/hystrix.stream端点的数据聚合到一个组合的/turbine.stream中，从而让集群的监控更加方便。
1. 添加依赖。
~~~
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-turbine</artifactId>
</dependency>
~~~
2. 编写启动类。
~~~
@EnableTurbine
@SpringBootApplication(scanBasePackages = "com.github.mg0324")
public class StartupApplication {
    public static void main(String[] args) {
        SpringApplication.run(StartupApplication.class,args);
    }
}
~~~
3. 添加配置。
~~~
server:
  port: 8031
spring:
  application:
    name: card-hystrix-turbine
eureka:
  client:
    service-url:
      defaultZone: http://192.168.3.29:8761/eureka/
  instance:
    prefer-ip-address: true
turbine:
  # 要监控的微服务列表，多个用,分隔
  appConfig: mic-card,mic-test
  clusterNameExpression: "'default'"
~~~
4. 启动服务后，得到 http://192.168.3.29:8031/turbine.stream 的聚合节点。
5. 填写到hystrix dashboard的url中做监控。

![](/mb/images/sc/rdq/turbine.png)

## 参考
https://www.itmuch.com/spring-cloud/finchley-15/
