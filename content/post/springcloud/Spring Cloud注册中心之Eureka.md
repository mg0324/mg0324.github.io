---
title: "Spring Cloud注册中心之Eureka"
date: 2022-01-20T00:12:17+08:00
draft: false
categories: ["技术文章","Spring Cloud"]
tags: ["Spring Cloud","微服务"]
---

## Eureka介绍
Spring Cloud Euraka是Spring Cloud集合中一个组件，它是对Euraka的集成，用于服务注册和发现。Eureka是Netflix中的一个开源框架。它和 zookeeper、Consul一样，都是用于服务注册管理的，同样，Spring Cloud 还集成了Zookeeper和Consul。

Eureka由多个instance(服务实例)组成，这些服务实例可以分为两种：Eureka Server和Eureka Client。为了便于理解，我们将Eureka client再分为Service Provider和Service Consumer。

*   Eureka Server 提供服务注册和发现
*   Service Provider 服务提供方，将自身服务注册到Eureka，从而使服务消费方能够找到
*   Service Consumer服务消费方，从Eureka获取注册服务列表，从而能够消费服务

补充：
Spring Cloud最早的注册中心，目前已经进入`停更进维`了，但是还是建议玩一玩，毕竟还是有部分公司还是用Eureka来做注册中心的。

## 集成Eureka
注意本文使用的版本：
``` xml
<spring-cloud.version>Hoxton.SR10</spring-cloud.version>
<spring-boot-version>2.2.7.RELEASE</spring-boot-version>
```
### 编写Eureka Server端
#### 1.添加eureka-server依赖
``` xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
</dependency>
```

#### 2. 创建启动类,加上`@EnableEurekaServer`注解
``` java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;

/**
 * @Description eureka启动类
 * @Date 2021-11-30 20:55
 * @Created by mango
 */
@EnableEurekaServer
@SpringBootApplication(scanBasePackages = "com.github.mg0324")
public class StartupApplication {
    public static void main(String[] args) {
        SpringApplication.run(StartupApplication.class,args);
    }
}
```
#### 3. 添加配置文件`application.yml`
``` yml
server:
  port: 8761
eureka:
  client:
    # 是否要注册到其他Eureka Server实例
    register-with-eureka: false
    # 是否要从其他Eureka Server实例获取数据
    fetch-registry: false
    service-url:
      defaultZone: http://localhost:8761/eureka/
```

#### 4.启动 Eureka Server
访问 `http://localhost:8761`
![](/mb/images/sc/register/eureka.png)
 
### 客户端集成Eureka Client
#### 1.pom.xml中添加依赖
``` xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```
#### 2. 添加配置项
``` yml
eureka:
  client:
    registryFetchIntervalSeconds: 10
    serviceUrl:
      defaultZone: http://127.0.0.1:8761/eureka/
    # 是否注册IP到eureka server，如不指定或设为false，那就会注册主机名到eureka server
    prefer-ip-address: true
```
Spring Cloud版本 `Hoxton.SR10` 不需要在启动类上添加 `@EnableDiscoveryClient`注解了。
#### 3.启动客户端
查看Eureka界面，可以看到微服务列表有服务注册成功。
![](/mb/images/sc/register/eureka_client.png)

也阔以从`spring boot admin server`里看到，如下图：
![](/mb/images/sc/register/sbAdminServer.png)

