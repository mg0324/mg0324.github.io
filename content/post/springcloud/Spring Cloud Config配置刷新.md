---
title: "Spring Cloud Config配置刷新"
date: 2022-01-22T12:22:58+08:00
draft: false
categories: ["技术文章","Spring Cloud"]
tags: ["Spring Cloud","微服务"]
---

## 配置刷新
实际项目中，加入了配置中心后，config client都连接config server，config server 连接git仓库（或者其他存储），配置修改后需要更新到config client。
如此，config client就不需要重新启动，也能应用到最新的配置。

## 配置刷新3要素
1.  config client依赖中有`spring-boot-starter-actuator`
2. 暴露了refresh节点
``` yaml
management:  
    endpoints:  
        web:  
            exposure:  
                include: refresh
```
3. 待刷新类上有注解`@RefreshScope`
~~~ java
@RestController
@RequestMapping("/test")
@Slf4j
@RefreshScope
public class TestController {
    @Value("${config.value}")
    private String config;

    @GetMapping("/config/get")
    public String testConfig(){
        return config;
    }

}
~~~
4. 配置修改后，手动请求config client的refresh刷新配置。
~~~
config:
  value: 变化123!加了变化
~~~
然后手动刷新。
```
(mango) mango@mangodeMacBook-Pro plan % curl -X POST http://127.0.0.1:9202/actuator/refresh
["config.client.version","config.value"]%
```
（自动刷新，参考文档：[http://www.itmuch.com/spring-cloud/spring-cloud-bus-auto-refresh-configuration/](http://www.itmuch.com/spring-cloud/spring-cloud-bus-auto-refresh-configuration/)
引入Cloud Bus后，就会多一个`/actuator/bus-refresh`端点）
5. 访问 http://127.0.0.1:9201/test/test/config/get，查看配置是否刷新 
![](/mb/images/sc/config/05.png)

如上，配置已经修改！