---
title: "Spring Cloud集成Admin Server"
date: 2022-01-19T12:29:02+08:00
draft: false
categories: ["技术文章","Spring Cloud"]
tags: ["Spring Cloud","微服务"]
---

## spring cloud集成spring boot admin server 
在这篇文章[Springboot集成Actuator和SpringbootAdminServer监控](https://www.kancloud.cn/mangomei/deepstudy/2568509)，我们学到了在`spring boot`应用中集成`spring boot admin server`来UI化显示`spring boot actuator`的`endpoint`数据。

那如果是spring cloud应用呢？如何将集成`spring boot admin server`来界面化显示应用的指标数据呢？

### card-admin-server集成spring boot admin server
1. 添加依赖
~~~
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-logging</artifactId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
<dependency>
    <groupId>de.codecentric</groupId>
    <artifactId>spring-boot-admin-starter-server</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
~~~
2. 创建启动类，注意机上注解`@EnableAdminServer`
~~~
@EnableAdminServer
@SpringBootApplication(scanBasePackages = "com.github.mg0324")
public class StartupApplication {
    public static void main(String[] args) {
        SpringApplication.run(StartupApplication.class,args);
    }
}
~~~
3. 添加安全配置类
~~~
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        SavedRequestAwareAuthenticationSuccessHandler successHandler
            = new SavedRequestAwareAuthenticationSuccessHandler();
        successHandler.setTargetUrlParameter("redirectTo");
        successHandler.setDefaultTargetUrl("/");

        http.authorizeRequests()
            .antMatchers("/assets/**").permitAll()
            .antMatchers("/login").permitAll()
            .anyRequest().authenticated().and()
            .formLogin().loginPage("/login")
            .successHandler(successHandler).and()
            .logout().logoutUrl("/logout").and()
            .httpBasic().and()
            .csrf()
            .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
            .ignoringAntMatchers(
                "/instances",
                "/actuator/**"
             );
    }
}
~~~
4. 设置配置
~~~
server:
    port: 8100
    servlet:
        context-path: /
spring:
    application:
        name: card-admin-server
    security:
        user:
            name: admin
            password: 123456

eureka:
    instance:
        leaseRenewalIntervalInSeconds: 10
        health-check-url-path: /actuator/health
        metadata-map:
            user.name: admin
            user.password: 123456
    client:
        registryFetchIntervalSeconds: 10
        serviceUrl:
            #defaultZone: http://192.168.3.26:8761/eureka/
            defaultZone: http://127.0.0.1:8761/eureka/

management:
    endpoint:
        health:
            show-details: always
    endpoints:
        web:
            exposure:
                include: '*'
~~~
5. 启动访问
![](/mb/images/sc/watch/adminServer.png)

## 总结
1. springboot应用界面显示的是程序中使用的中间件状态；spring cloud应用显示的是微服务相关的组件的状态。
2. 都是基于springboot actuator的endpoint数据做界面展示的。
