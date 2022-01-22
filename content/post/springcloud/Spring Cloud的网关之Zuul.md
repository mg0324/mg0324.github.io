---
title: "Spring Cloud的网关之Zuul"
date: 2022-01-22T10:58:06+08:00
draft: false
categories: ["技术文章","Spring Cloud"]
tags: ["Spring Cloud","微服务"]
---

本文只是简单的zuul入门，尝尝鲜！
## Zuul简介
Zuul是Netflix开源的微服务网关，它可以和Eureka、Ribbon、Hystrix等组件配合使用。Zuul的核心是一系列的过滤器，这些过滤器帮助我们完成以下功能：

*   身份认证与安全：识别每个资源的验证要求，并拒绝那些与要求不符的请求；
*   审查与监控：在边缘位置追踪有意义的数据和统计结果，从而为我们带来精确的生产视图；
*   动态路由：动态地将请求路由到不同的后端集群；
*   压力测试：逐渐增加指向集群的流量，以了解性能；
*   负载分配：为每一种负载类型分配对应容量，并弃用超出限定值的请求；
*   静态响应处理：在边缘位置直接建立部分响应，从而避免其转发到内部集群；
*   多区域弹性：跨越AWS Region进行请求路由，旨在实现ELB（Elastic Load Balancing）使用的多样化；以及让系统的边缘更贴近系统的使用者。

## 集成zuul
1. 添加依赖
~~~
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-zuul</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
~~~
2. 添加失败处理器
~~~
@Component
public class MyFallbackProvider implements FallbackProvider {
  @Override
  public String getRoute() {
    // 表明是为哪个微服务提供回退，*表示为所有微服务提供回退
    return "*";
  }

  @Override
  public ClientHttpResponse fallbackResponse(String route, Throwable cause) {
    if (cause instanceof HystrixTimeoutException) {
      return response(HttpStatus.GATEWAY_TIMEOUT);
    } else {
      return this.fallbackResponse();
    }
  }

  public ClientHttpResponse fallbackResponse() {
    return this.response(HttpStatus.INTERNAL_SERVER_ERROR);
  }

  private ClientHttpResponse response(final HttpStatus status) {
    return new ClientHttpResponse() {
      @Override
      public HttpStatus getStatusCode() throws IOException {
        return status;
      }

      @Override
      public int getRawStatusCode() throws IOException {
        return status.value();
      }

      @Override
      public String getStatusText() throws IOException {
        return status.getReasonPhrase();
      }

      @Override
      public void close() {
      }

      @Override
      public InputStream getBody() throws IOException {
        return new ByteArrayInputStream("服务不可用，请稍后再试。".getBytes());
      }

      @Override
      public HttpHeaders getHeaders() {
        // headers设定
        HttpHeaders headers = new HttpHeaders();
        MediaType mt = new MediaType("application", "json", Charset.forName("UTF-8"));
        headers.setContentType(mt);
        return headers;
      }
    };
  }
}
~~~
3. 编写启动类，添加注解`@EnableZuulProxy`
~~~
@EnableZuulProxy
@SpringBootApplication(scanBasePackages = "com.github.mg0324")
public class StartupApplication {
    public static void main(String[] args) {
        SpringApplication.run(StartupApplication.class,args);
    }
}
~~~
4. 添加配置
~~~
server:
  port: 8040

eureka:
  client:
    service-url:
      defaultZone: http://192.168.3.26:8761/eureka/

management:
  endpoints:
    web:
      exposure:
        include: '*'
  endpoint:
    health:
      show-details: always

logging:
  level:
    com.netflix: DEBUG
# 配置路由
zuul:
  routes:
    mic-card:
      path: /card/**
      strip-prefix: false
    mic-test:
      path: /test/**
      strip-prefix: false
  #prefix: /gateway
~~~
5. 启动mic-card的微服务，并访问测试 http://127.0.0.1:8040/card/admin/card/rand
![](/mb/images/sc/gateway/zuul00.png)
![](/mb/images/sc/gateway/zuul01.png)

## 总结
* zuul只是spring cloud全家桶里的网关的一种实现，后续还有gateway。
* 其中路由的配置最重要，网关能对路由做相关编排实现。
