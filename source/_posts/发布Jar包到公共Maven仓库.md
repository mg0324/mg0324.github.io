---
title: 发布Jar包到公共Maven仓库
categories:
  - java
tags:
  - java
  - maven
  - jar发布
abbrlink: 66be94d7
date: 2021-12-12 16:48:00
---

# 起因
自己写了个简单的框架，想要发布到公共的maven仓库上，方便自己引用，也给其他开发者创造一个轮子。

# 参考鸣谢
1. 流程 https://blog.csdn.net/qq_36838191/article/details/81027586
2. 操作 https://www.cnblogs.com/newsea/p/11604171.html

<!-- more -->

# 几个地址
*   工单管理：[https://issues.sonatype.org](https://issues.sonatype.org/)
*   构件仓库 : [https://oss.sonatype.org/#welcome](https://oss.sonatype.org/#welcome)
*   仓库镜像: [http://search.maven.org/](http://search.maven.org/)

# 发布流程
1. 创建工单
2. 发布jar包
3. 审核通过（2小时后能在中央仓库搜索到）

# 步骤
## 1.创建工单

![](/mb/images/java/jar-01.png)

## 2.发布jar包
Idea Maven项目集成发布插件
### pom.xml文件添加信息
项目描述
``` xml
<name>mango-admin-dependencies</name>
<url>https://github.com/mg0324/mango-admin-dependencies</url>
<description>mango admin dependencies</description>
```
licenses + scm信息
``` xml
<licenses>
    <license>
        <name>The Apache Software License, Version 2.0</name>
        <url>http://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
</licenses>
<scm>
    <connection>scm:git:git://github.com/mg0324/mango-admin-dependencies.git</connection>
    <developerConnection>scm:git:ssh://github.com/mg0324/mango-admin-dependencies.git</developerConnection>
    <url>https://github.com/mg0324/mango-admin-dependencies/tree/main</url>
</scm>
```
开发者信息 + 贡献仓库地址
``` xml
<developers>
    <developer>
        <name>mangomei</name>
        <id>mangomei</id>
        <email>1092017732@qq.com</email>
        <roles>
            <role>Developer</role>
        </roles>
        <timezone>+8</timezone>
    </developer>
</developers>
<distributionManagement>
    <snapshotRepository>
        <id>ossrh</id>
        <url>https://oss.sonatype.org/content/repositories/snapshots/</url>
    </snapshotRepository>
    <repository>
        <id>ossrh</id>
        <url>https://oss.sonatype.org/service/local/staging/deploy/maven2/</url>
    </repository>
</distributionManagement>
```
构建信息及插件
``` xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>2.3.2</version>
            <configuration>
                <source>1.8</source>
                <target>1.8</target>
                <encoding>UTF-8</encoding>
            </configuration>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-resources-plugin</artifactId>
            <version>2.5</version>
            <configuration>
                <encoding>UTF-8</encoding>
                <nonFilteredFileExtensions>
                    <nonFilteredFileExtension>dat</nonFilteredFileExtension>
                </nonFilteredFileExtensions>
                <outputDirectory />
            </configuration>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-source-plugin</artifactId>
            <version>2.1.2</version>
            <executions>
                <execution>
                    <id>attach-sources</id>
                    <phase>verify</phase>
                    <goals>
                        <goal>jar-no-fork</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-javadoc-plugin</artifactId>
            <version>2.9.1</version>
            <executions>
                <execution>
                    <id>attach-javadocs</id>
                    <goals>
                        <goal>jar</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-gpg-plugin</artifactId>
            <version>1.5</version>
            <executions>
                <execution>
                    <id>sign-artifacts</id>
                    <phase>verify</phase>
                    <goals>
                        <goal>sign</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>versions-maven-plugin</artifactId>
            <configuration>
                <generateBackupPoms>false</generateBackupPoms>
            </configuration>
        </plugin>
        <plugin>
            <groupId>org.sonatype.plugins</groupId>
            <artifactId>nexus-staging-maven-plugin</artifactId>
            <version>1.6.7</version>
            <extensions>true</extensions>
            <configuration>
                <serverId>ossrh</serverId>
                <nexusUrl>https://oss.sonatype.org/</nexusUrl>
                <autoReleaseAfterClose>true</autoReleaseAfterClose>
            </configuration>
        </plugin>
    </plugins>
</build>
```
### Maven的配置文件setting.xml新增
该账号为工单系统账号。（需要自己注册）
``` xml
<server>
    <id>ossrh</id>
    <username>mangomei</username>
    <password>123456</password>
</server>
```
注意：
按上述模板信息，修改为自己的项目信息。其中自己的项目地址，开发者和账号信息必须设置。

### 执行Maven发布命令
``` bash
mvn deploy
```
发布成功后，能在 https://search.maven.org/search 里搜索到自己的包。

![](/mb/images/java/jar-02.png)

## 审核通过
审核通过后，工单会变成已解决的状态（之前会收到邮件提醒），提示内容为，你的包已经发布成功，在2小时候后能在中央仓库查到。

![](/mb/images/java/jar-03.png)