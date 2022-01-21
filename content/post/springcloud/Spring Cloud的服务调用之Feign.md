---
title: "SpringCloud的服务调用之Feign"
date: 2022-01-21T22:51:51+08:00
draft: false
categories: ["技术文章","Spring Cloud"]
tags: ["Spring Cloud","微服务"]
---

## Feign介绍
如果只用Ribbon里的RestTemplate来调用，会发现URL，参数返回值等都需要写死。
``` java
ResultObject<CardVo> result = (ResultObject<CardVo>) restTemplate.getForObject(
        "http://mic-card/card/admin/card/rand",
        ResultObject.class
);
```
如果服务提供者做了调整，则代码变得难以维护。

Feign组件出现，声明式解决上述问题。
Feign是Netflix公司开发的声明式、模板式的HTTP客户端，能够帮助你优雅的调用HTTP API。

## Feign集成
注意本文使用的版本：
``` xml
<spring-cloud.version>Hoxton.SR10</spring-cloud.version>
<spring-boot-version>2.2.7.RELEASE</spring-boot-version>
```
### 1.添加Feign依赖
``` xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```
### 2.使用FeignClient来调用微服务
``` java
@FeignClient(name = "mic-card",path = "/card/admin")
public interface CardApi {

    @GetMapping("/card/rand")
    ResultObject<CardVo> getRand();

}
```
Controller中调用
``` java
@Autowired
private CardApi cardApi;

@GetMapping("/feign/cardRand")
public Result feignCardRand(){
    return cardApi.getRand();
}
```
### 3.访问验证
![](/mb/images/sc/feign/01.png)

## Feign深入
参考： https://www.itmuch.com/spring-cloud/finchley-10/


