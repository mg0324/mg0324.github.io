---
title: "Spring Cloud熔断器之Hystrix"
date: 2022-01-21T23:15:24+08:00
draft: false
categories: ["技术文章","Spring Cloud"]
tags: ["Spring Cloud","微服务"]
---

## Hystrix介绍
Hystrix是由Netflix开源的一个延迟和容错库，用于隔离访问远程系统、服务或者第三方库，防止级联失败，从而提升系统的可用性与容错性。

### Hystrix特性
Hystrix主要通过以下几点实现延迟和容错。
* 包裹请求 - `@HystrixCommand`注解（命令模式）
* 跳闸机制 - 5秒内20次失败，一段时间内会停止访问服务
* 资源隔离 - 给每个服务提供小型线程池，线程池满立即拒绝请求
* 监控
* 回退机制 - 开发人员可提供默认回退逻辑
* 自我修复 - 一段时间内，会尝试调用一次服务，请求成功则关闭断路器

## Hystrix 集成
### 添加依赖
``` xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
</dependency>
```
### 开启断路器
在启动类上增加`@EnableHystrix`注解或者`@EnableCircuitBreaker`注解。

### 直接使用`@HystrixCommand`
``` java
@FeignClient(name = "mic-card",path = "/card/admin")
public interface CardApi {

    @PostMapping("/count/home")
    @HystrixCommand
    ResultObject<CountVo> getHome();
}
```

### 结合Feign使用
Feign默认是不启用Hystrix的，添加如下配置启用。
``` yml
feign:
  hystrix:
    enabled: true
```
``` java
/**
 * @Description card api服务
 * @Date 2021-12-04 10:12
 * @Created by mango
 */
@FeignClient(name = "mic-card",path = "/card/admin",
        configuration = {FeignConfiguration.class},
        fallback = CardApiFallback.class)
public interface CardApi {

    @GetMapping("/card/rand")
    ResultObject<CardVo> getRand();

    @PostMapping("/count/home")
    ResultObject<CountVo> getHome();
}

## 回退机制，自定义实现回退逻辑
@Component
@Slf4j
class CardApiFallback implements CardApi {
    @Autowired
    private ResultUtil resultUtil;
    @Override
    public ResultObject<CardVo> getRand() {
        log.info("enter card api fallback");
        CardVo cardVo = new CardVo();
        cardVo.setName("enter fallback");
        cardVo.setIsOpen("1");
        cardVo.setCreateTime(DateUtil.now());
        return resultUtil.success2obj(cardVo,"success");
    }

    @Override
    public ResultObject<CountVo> getHome() {
        log.info("enter card api get home fallback");
        CountVo countVo = new CountVo();
        countVo.setCardCount(1);
        countVo.setFileCount(1);
        countVo.setPointCount(1);
        return resultUtil.success2obj(countVo,"success");
    }
}
```
## 配置相关
### 全局启用
~~~
feign.hystrix.enabled: true
~~~
#### 全局禁用
~~~
feign.hystrix.enabled: false
~~~
### 局部启用
~~~
public class FeignEnableHystrixConfiguration {
    @Bean
	@Scope("prototype")
	public HystrixFeign.Builder feignBuilder() {
		return HystrixFeign.builder();
	}
}
~~~
~~~
@FeignClient(name = "mic-card",path = "/card/admin",
        configuration = {FeignEnableHystrixConfiguration.class},
        fallback = CardApiFallback.class)
~~~

## 局部禁用
~~~
public class FeignDisableHystrixConfiguration {
    @Bean
	@Scope("prototype")
	public Feign.Builder feignBuilder() {
		return Feign.builder();
	}
}
~~~
## @HystrixCommand注解源码
``` java
/**
 * This annotation used to specify some methods which should be processes as hystrix commands.
 */
@Target({ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Inherited
@Documented
public @interface HystrixCommand {

    /**
     * The command group key is used for grouping together commands such as for reporting,
     * alerting, dashboards or team/library ownership.
     * <p/>
     * default => the runtime class name of annotated method
     *
     * @return group key
     */
    String groupKey() default "";

    /**
     * Hystrix command key.
     * <p/>
     * default => the name of annotated method. for example:
     * <code>
     *     ...
     *     @HystrixCommand
     *     public User getUserById(...)
     *     ...
     *     the command name will be: 'getUserById'
     * </code>
     *
     * @return command key
     */
    String commandKey() default "";

    /**
     * The thread-pool key is used to represent a
     * HystrixThreadPool for monitoring, metrics publishing, caching and other such uses.
     *
     * @return thread pool key
     */
    String threadPoolKey() default "";

    /**
     * Specifies a method to process fallback logic.
     * A fallback method should be defined in the same class where is HystrixCommand.
     * Also a fallback method should have same signature to a method which was invoked as hystrix command.
     * for example:
     * <code>
     *      @HystrixCommand(fallbackMethod = "getByIdFallback")
     *      public String getById(String id) {...}
     *
     *      private String getByIdFallback(String id) {...}
     * </code>
     * Also a fallback method can be annotated with {@link HystrixCommand}
     * <p/>
     * default => see {@link com.netflix.hystrix.contrib.javanica.command.GenericCommand#getFallback()}
     *
     * @return method name
     */
    String fallbackMethod() default "";

    /**
     * Specifies command properties.
     *
     * @return command properties
     */
    HystrixProperty[] commandProperties() default {};

    /**
     * Specifies thread pool properties.
     *
     * @return thread pool properties
     */
    HystrixProperty[] threadPoolProperties() default {};

    /**
     * Defines exceptions which should be ignored.
     * Optionally these can be wrapped in HystrixRuntimeException if raiseHystrixExceptions contains RUNTIME_EXCEPTION.
     *
     * @return exceptions to ignore
     */
    Class<? extends Throwable>[] ignoreExceptions() default {};

    /**
     * Specifies the mode that should be used to execute hystrix observable command.
     * For more information see {@link ObservableExecutionMode}.
     *
     * @return observable execution mode
     */
    ObservableExecutionMode observableExecutionMode() default ObservableExecutionMode.EAGER;

    /**
     * When includes RUNTIME_EXCEPTION, any exceptions that are not ignored are wrapped in HystrixRuntimeException.
     *
     * @return exceptions to wrap
     */
    HystrixException[] raiseHystrixExceptions() default {};

    /**
     * Specifies default fallback method for the command. If both {@link #fallbackMethod} and {@link #defaultFallback}
     * methods are specified then specific one is used.
     * note: default fallback method cannot have parameters, return type should be compatible with command return type.
     *
     * @return the name of default fallback method
     */
    String defaultFallback() default "";
}
```

## 参考资料
* https://www.itmuch.com/spring-cloud/finchley-13/


