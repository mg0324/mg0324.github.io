---
title: springboot集成logback做日志分割
date: 2020-11-15 21:00:21
categories: ["技术文章"]
tags: ["springboot","logback","日志处理"]
draft: false
---

## 前提

> logback和log4j都能实现如下功能，下方给出logback配置。（测试是否更新。）

* 日志按天切割，并且设置最大容量。
* 日志配置文件修改，能热加载。
* 日志按包前缀分文件。（也能实现）


## logback配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration scan="true" scanPeriod="60 seconds" debug="true">
    <!--定义日志文件的存储地址 勿在 LogBack 的配置中使用相对路径-->
    <property name="LOG_HOME" value="./logs" />
    <!-- 控制台输出 -->
    <!--<appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
            &lt;!&ndash;格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符&ndash;&gt;
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg  %n</pattern>
        </encoder>
    </appender>-->
    <!-- 按照每天生成日志文件 -->
    <appender name="FILE"  class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_HOME}/madmin.log</file>
        <append>true</append>
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <fileNamePattern>${LOG_HOME}/madmin.log.%d{yyyy-MM-dd}-%i.log</fileNamePattern>
            <maxFileSize>100MB</maxFileSize>
            <maxHistory>30</maxHistory>
            <totalSizeCap>1GB</totalSizeCap>
        </rollingPolicy>
        <!--<rollingPolicy class="ch.qos.logback.core.rolling.FixedWindowRollingPolicy">
            <fileNamePattern>testFile.%i.log.zip</fileNamePattern>
            <minIndex>1</minIndex>
            <maxIndex>3</maxIndex>
        </rollingPolicy>-->
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
            <!--格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符-->
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg  %n</pattern>
        </encoder>
        <!--<filter class="ch.qos.logback.classic.filter.ThresholdFilter">
            <level>info</level>
        </filter>-->
    </appender>

    <logger name="com.github.mg0324" level="debug"/>
    <logger name="com.baomidou.mybatisplus" level="error"/>
    <logger name="org" level="error"/>
    <!-- 日志输出级别 -->
    <root level="debug">
        <appender-ref ref="FILE" />
    </root>
</configuration>
```

