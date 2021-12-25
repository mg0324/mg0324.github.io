---
title: apache-tomcat-8.0.43源码编译
categories: 源码
tags:
  - tomcat
  - 源码编译
abbrlink: 10b625fd
date: 2020-11-15 17:07:13
---

# 源码下载

到https://archive.apache.org/dist/tomcat/tomcat-8/v8.0.43/src/  下载对应版本源码，本文编译的是`apache-tomcat-8.0.43-src`

<!-- more-->

# 用idea 来编译

* 在`src`目录下加入`pom.xml`文件，使用`maven`来编译。

  ```
  <?xml version="1.0" encoding="UTF-8"?>
  <project xmlns="http://maven.apache.org/POM/4.0.0"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  
      <modelVersion>4.0.0</modelVersion>
      <groupId>org.apache.tomcat</groupId>
      <artifactId>Tomcat8.0</artifactId>
      <name>Tomcat8.0</name>
      <version>8.0</version>
  
      <build>
          <finalName>Tomcat8.0</finalName>
          <sourceDirectory>java</sourceDirectory>
          <testSourceDirectory>test</testSourceDirectory>
          <resources>
              <resource>
                  <directory>java</directory>
              </resource>
          </resources>
         <!-- <testResources>
              <testResource>
                  <directory>test</directory>
              </testResource>
          </testResources>-->
          <plugins>
              <plugin>
                  <groupId>org.apache.maven.plugins</groupId>
                  <artifactId>maven-compiler-plugin</artifactId>
                  <version>2.3</version>
                  <configuration>
                      <encoding>UTF-8</encoding>
                      <source>1.8</source>
                      <target>1.8</target>
                      <skip>true</skip>
                  </configuration>
              </plugin>
              <plugin>
                  <groupId>org.apache.maven.plugins</groupId>
                  <artifactId>maven-surefire-plugin</artifactId>
                  <version>2.5</version>
                  <configuration>
                      <skip>true</skip>
                  </configuration>
              </plugin>
          </plugins>
      </build>
  
      <dependencies>
          <dependency>
              <groupId>junit</groupId>
              <artifactId>junit</artifactId>
              <version>4.12</version>
              <scope>test</scope>
          </dependency>
          <dependency>
              <groupId>org.easymock</groupId>
              <artifactId>easymock</artifactId>
              <version>3.4</version>
          </dependency>
          <dependency>
              <groupId>ant</groupId>
              <artifactId>ant</artifactId>
              <version>1.7.0</version>
          </dependency>
          <dependency>
              <groupId>wsdl4j</groupId>
              <artifactId>wsdl4j</artifactId>
              <version>1.6.2</version>
          </dependency>
          <dependency>
              <groupId>javax.xml</groupId>
              <artifactId>jaxrpc</artifactId>
              <version>1.1</version>
          </dependency>
          <dependency>
              <groupId>org.eclipse.jdt.core.compiler</groupId>
              <artifactId>ecj</artifactId>
              <version>4.5.1</version>
          </dependency>
  
      </dependencies>
  </project>
  ```

* 在执行了clean和install后，尝试运行Bootstarp类。

  ```
  十一月 15, 2020 5:13:19 下午 org.apache.catalina.startup.CatalinaProperties loadProperties
  警告: Failed to load catalina.properties
  十一月 15, 2020 5:13:19 下午 org.apache.catalina.startup.Catalina load
  警告: Unable to load server configuration from [/Users/mango/git/src-code/conf/server.xml]
  十一月 15, 2020 5:13:19 下午 org.apache.catalina.startup.Catalina load
  警告: Unable to load server configuration from [/Users/mango/git/src-code/conf/server.xml]
  十一月 15, 2020 5:13:19 下午 org.apache.catalina.startup.Catalina start
  严重: Cannot start server. Server instance is not configured.
  
  Process finished with exit code 0
  ```

  如果出现上述问题，需要设置启动目录，如下图。

  ![](https://mangomei.oss-cn-shenzhen.aliyuncs.com/tomcat/tomcat8-1.png)

* 运行后打印出运行在8080端口后，尝试访问 http://localhost:8080。出现如下问题：

  ![](https://mangomei.oss-cn-shenzhen.aliyuncs.com/tomcat/tomcat8-2.png)

需要在Bootstarp.java最前面加上如下代码：（参考：https://www.jianshu.com/p/771df8a99505）

```
{
	JasperInitializer jasperInitializer = new JasperInitializer();
}
```

![](https://mangomei.oss-cn-shenzhen.aliyuncs.com/tomcat/tomcat8-3.png)

* 再次运行发现中间加载example的时候报错，先不管。访问 http://localhost:8080  出现如下图则说明tomcat源码运行成功，可以做源码断点学习调试了。恭喜您！

  ![](https://mangomei.oss-cn-shenzhen.aliyuncs.com/tomcat/tomcat8-4.png)

# example的加载错误

错误如下：类没有找到。

```
十一月 15, 2020 5:25:07 下午 org.apache.catalina.startup.HostConfig deployDirectory
信息: Deploying web application directory /Users/mango/git/src-code/apache-tomcat-8.0.43-src/webapps/examples
十一月 15, 2020 5:25:07 下午 org.apache.catalina.core.StandardContext listenerStart
严重: Error configuring application listener of class listeners.ContextListener
java.lang.ClassNotFoundException: listeners.ContextListener
	at org.apache.catalina.loader.WebappClassLoaderBase.loadClass(WebappClassLoaderBase.java:1333)
	at org.apache.catalina.loader.WebappClassLoaderBase.loadClass(WebappClassLoaderBase.java:1167)
	at org.apache.catalina.core.DefaultInstanceManager.loadClass(DefaultInstanceManager.java:509)
	at org.apache.catalina.core.DefaultInstanceManager.loadClassMaybePrivileged(DefaultInstanceManager.java:490)
	at org.apache.catalina.core.DefaultInstanceManager.newInstance(DefaultInstanceManager.java:118)
	at org.apache.catalina.core.StandardContext.listenerStart(StandardContext.java:4775)
	at org.apache.catalina.core.StandardContext.startInternal(StandardContext.java:5314)
	at org.apache.catalina.util.LifecycleBase.start(LifecycleBase.java:145)
	at org.apache.catalina.core.ContainerBase.addChildInternal(ContainerBase.java:753)
	at org.apache.catalina.core.ContainerBase.addChild(ContainerBase.java:729)
	at org.apache.catalina.core.StandardHost.addChild(StandardHost.java:717)
	at org.apache.catalina.startup.HostConfig.deployDirectory(HostConfig.java:1092)
	at org.apache.catalina.startup.HostConfig$DeployDirectory.run(HostConfig.java:1834)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run$$$capture(FutureTask.java:266)
	at java.util.concurrent.FutureTask.run(FutureTask.java)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
```

在网上百度了下，有篇文章说直接删掉，我晕哦，这是在逃避。

仔细看了下，就是类没有找到，发现下载的包里的example是源码，里面的classes下放的是Java文件，需要编译。

# 给example做编译

在webapps/example/WEB-INF目录下加入pom.xml文件。然后执行clean和install，将得到的class文件放到原来的classes下，再次启动加载成功。哈哈。

```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>
    <groupId>org.apache.tomcat</groupId>
    <artifactId>Tomcat8.0-example</artifactId>
    <name>Tomcat8.0 example</name>
    <version>1.0</version>

    <build>
        <finalName>Tomcat8.0-example</finalName>
        <sourceDirectory>classes</sourceDirectory>
        <resources>
            <resource>
                <directory>classes</directory>
            </resource>
        </resources>
        <!-- <testResources>
             <testResource>
                 <directory>test</directory>
             </testResource>
         </testResources>-->
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>2.3</version>
                <configuration>
                    <encoding>UTF-8</encoding>
                    <source>1.8</source>
                    <target>1.8</target>
                    <skip>true</skip>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>2.5</version>
                <configuration>
                    <skip>true</skip>
                </configuration>
            </plugin>
        </plugins>
    </build>

    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.12</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.apache.tomcat</groupId>
            <artifactId>Tomcat8.0</artifactId>
            <version>8.0</version>
            <scope>compile</scope>
        </dependency>

    </dependencies>
</project>
```

![](https://mangomei.oss-cn-shenzhen.aliyuncs.com/tomcat/tomcat8-5.png)

再次运行成功。

```
信息: Deploying web application directory /Users/mango/git/src-code/apache-tomcat-8.0.43-src/webapps/examples
十一月 15, 2020 5:42:29 下午 org.apache.catalina.core.ApplicationContext log
信息: ContextListener: contextInitialized()
十一月 15, 2020 5:42:29 下午 org.apache.catalina.core.ApplicationContext log
信息: SessionListener: contextInitialized()
十一月 15, 2020 5:42:29 下午 org.apache.catalina.startup.HostConfig deployDirectory
信息: Deployment of web application directory /Users/mango/git/src-code/apache-tomcat-8.0.43-src/webapps/examples has finished in 124 ms
十一月 15, 2020 5:42:29 下午 org.apache.catalina.startup.HostConfig deployDirectory
信息: Deploying web application directory /Users/mango/git/src-code/apache-tomcat-8.0.43-src/webapps/ROOT
十一月 15, 2020 5:42:30 下午 org.apache.catalina.startup.HostConfig deployDirectory
信息: Deployment of web application directory /Users/mango/git/src-code/apache-tomcat-8.0.43-src/webapps/ROOT has finished in 66 ms
十一月 15, 2020 5:42:30 下午 org.apache.catalina.startup.HostConfig deployDirectory
信息: Deploying web application directory /Users/mango/git/src-code/apache-tomcat-8.0.43-src/webapps/host-manager
十一月 15, 2020 5:42:30 下午 org.apache.catalina.startup.HostConfig deployDirectory
信息: Deployment of web application directory /Users/mango/git/src-code/apache-tomcat-8.0.43-src/webapps/host-manager has finished in 176 ms
十一月 15, 2020 5:42:30 下午 org.apache.coyote.AbstractProtocol start
信息: Starting ProtocolHandler ["http-nio-8080"]
十一月 15, 2020 5:42:30 下午 org.apache.coyote.AbstractProtocol start
信息: Starting ProtocolHandler ["ajp-nio-8009"]
十一月 15, 2020 5:42:30 下午 org.apache.catalina.startup.Catalina start
信息: Server startup in 1843 ms
```

