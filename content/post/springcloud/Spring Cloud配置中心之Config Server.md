---
title: "Spring Cloud配置中心之Config Server"
date: 2022-01-22T12:18:36+08:00
draft: false
categories: ["技术文章","Spring Cloud"]
tags: ["Spring Cloud","微服务"]
---

## spring cloud config简介
Spring Cloud Config为分布式系统外部化配置提供了服务器端和客户端的支持，它包括Config Server和Config Client两部分。

Config Server是一个可横向扩展、集中式的配置服务器，它用于集中管理应用程序各个环境下的配置，默认使用Git存储配置内容（也可使用Subversion、MySQL、本地文件系统或Vault存储配置，本博客以Git为例进行讲解），因此可以很方便地实现对配置的版本控制与内容审计。

![](/mb/images/sc/config/01.png)

## 远程gitee仓库
![](/mb/images/sc/config/02.png)

## 集成config server
1. 添加依赖
~~~
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-config-server</artifactId>
</dependency>
~~~
2. 编写启动类
~~~
@EnableConfigServer
@SpringBootApplication(scanBasePackages = "com.github.mg0324")
public class StartupApplication {
    public static void main(String[] args) {
        SpringApplication.run(StartupApplication.class,args);
    }
}
~~~
3. 设置配置 application.yaml
~~~
server:
  port: 8080
spring:
  application:
    name: card-config-server
  cloud:
    config:
      server:
        git:
          # Git仓库地址
          uri: https://gitee.com/mgang/card-config-repo.git
          # Git仓库账号
          username:
          # Git仓库密码
          password:

logging:
  level:
    com.netflix: DEBUG
~~~
4. 启动查看 http://127.0.0.1:8080/mic-test-dev.yaml
访问mic-test-dev.yaml会整合mic-test.yaml的内容。
![](/mb/images/sc/config/03.png)
### 路径规则
Spring Cloud Config Server提供了RESTful API，可用来访问存放在Git仓库中的配置文件。
``` 
/{application}/{profile}[/{label}]
/{application}-{profile}.yml
/{label}/{application}-{profile}.yml
/{application}-{profile}.properties
/{label}/{application}-{profile}.properties
```

## 集成Config Client
1. 添加依赖
~~~
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-config</artifactId>
</dependency>
~~~
2. 加配置：bootstrap.yml
~~~
spring:
  application:
    name: mic-test
  cloud:
    config:
      uri: http://127.0.0.1:8080/
      profile: dev            # profile对应config server所获取的配置文件中的{profile}
      label: master
~~~
3. 写代码访问
~~~
@Value("${config.value}")
private String config;

@GetMapping("/config/get")
public String testConfig(){
    return config;
}
~~~
4. 启动mic-test访问 http://127.0.0.1:9201/test/test/config/get 测试
![](/mb/images/sc/config/04.png)

## 总结
* Config Server连接git仓库，Config Client连接Config Server。
* Config Client获取配置属性@Value注解。