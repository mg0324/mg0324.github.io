---
title: maven打包dir目录暴露配置文件
categories: maven打包
tags:
  - maven
  - springboot
  - package
abbrlink: 2d127f5d
date: 2017-12-13 16:58:29
---

## 起因
> 在springboot框架下，打包项目发布最开始打包为整包，然后使用`java -jar xxx.jar --spring.profiles.active=w2n`的命令来启动。
但是之后更新项目时，都是以全量更新的方式，这样做如果只是修改了一点点代码需要更新的话，也得发一个全量包。如是做法，是不优雅的。所以
特此寻找到`maven的打包插件assembly`。
<!--more-->
## 主要内容
> 1.在打包的maven模块`pom.xml`中，添加如下配置

	<resources>
        <!-- 复制资源 -->
        <resource>
            <directory>src/main/resources</directory>
            <includes>
                <include>**/*</include>
            </includes>
        </resource>
    </resources>
    <plugins>
        <!-- 设置源文件编码方式 -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <configuration>
                <source>1.7</source>
                <target>1.7</target>
                <encoding>UTF-8</encoding>
            </configuration>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-jar-plugin</artifactId>
            <version>2.6</version>
            <!-- The configuration of the plugin -->
            <configuration>
                <!-- Configuration of the archiver -->
                <archive>

                    <!--
                        生成的jar中，不要包含pom.xml和pom.properties这两个文件
                    -->
                    <addMavenDescriptor>false</addMavenDescriptor>

                    <!-- Manifest specific configuration -->
                    <manifest>
                        <!--
                            是否要把第三方jar放到manifest的classpath中
                        -->
                        <addClasspath>true</addClasspath>
                        <!--
                           生成的manifest中classpath的前缀，因为要把第三方jar放到lib目录下，所以classpath的前缀是lib/
                       -->
                        <classpathPrefix>lib/</classpathPrefix>
                        <!--
                            应用的main class
                        -->
                        <mainClass>com.inspur.proxy.ZscProxyApplication</mainClass>
                    </manifest>
                    <manifestEntries>
                        <Class-Path>./</Class-Path>
                    </manifestEntries>
                </archive>
                <!--
                    过滤掉不希望包含在jar中的文件
                -->
                <!--<excludes>-->
                <!--<exclude>${project.basedir}/xml/*</exclude>-->
                <!--</excludes>-->
                <excludes>
                    <exclude>config/**</exclude>
                    <exclude>spring/**</exclude>
                    <exclude>*.properties</exclude>
                </excludes>
            </configuration>
        </plugin>

        <!-- The configuration of maven-assembly-plugin -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-assembly-plugin</artifactId>
            <version>2.4</version>
            <!-- The configuration of the plugin -->
            <configuration>
                <!-- Specifies the configuration file of the assembly plugin -->
                <descriptors>
                    <descriptor>src/main/resources/assembly/assembly.xml</descriptor>
                </descriptors>
            </configuration>
            <executions>
                <execution>
                    <id>make-assembly</id>
                    <phase>package</phase>
                    <goals>
                        <goal>single</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>

> 2.配置插件的`assembly.xml`文件


	<assembly>
	    <id>ga</id>
	    <includeBaseDirectory>false</includeBaseDirectory>
	    <!-- 最终打包成一个用于发布的zip文件 -->
	    <formats>
	        <format>dir</format>
	    </formats>
	    <!-- Adds dependencies to zip package under lib directory -->
	    <dependencySets>
	        <dependencySet>
	            <!--
	               不使用项目的artifact，第三方jar不要解压，打包进zip文件的lib目录
	           -->
	            <useProjectArtifact>false</useProjectArtifact>
	            <outputDirectory>lib</outputDirectory>
	            <unpack>false</unpack>
	        </dependencySet>
	    </dependencySets>

	    <fileSets>
	        <!-- 把项目相关的说明文件，打包进zip文件的根目录 -->
	        <!--<fileSet>-->
	        <!--<directory>${project.basedir}</directory>-->
	        <!--<outputDirectory>/</outputDirectory>-->
	        <!--</fileSet>-->

	        <!-- 把项目的配置文件，打包进zip文件的config目录 -->
	        <fileSet>
	            <directory>src/main/resources</directory>
	            <outputDirectory>/config</outputDirectory>
	            <includes>
	                <!--<include>*.xml</include>-->
	                <include>*.properties</include>
	            </includes>
	            <excludes>
	                <exclude>log4j.properties</exclude>
	            </excludes>
	        </fileSet>
	        <fileSet>
	            <directory>src/main/resources</directory>
	            <outputDirectory>/</outputDirectory>
	            <includes>
	                <!--<include>*.xml</include>-->
	                <include>log4j.properties</include>
	            </includes>
	        </fileSet>
	        <!--<fileSet>
	            <directory>src/main/resources/spring</directory>
	            <outputDirectory>/spring</outputDirectory>
	            <includes>
	                <include>*</include>
	            </includes>
	        </fileSet>-->
	        <fileSet>
	            <directory>src/main/resources/config</directory>
	            <outputDirectory>/config</outputDirectory>
	            <includes>
	                <include>*.properties</include>
	            </includes>
	        </fileSet>
	        <!-- 把项目自己编译出来的jar文件，打包进zip文件的根目录 -->
	        <fileSet>
	            <directory>${project.build.directory}</directory>
	            <outputDirectory></outputDirectory>
	            <includes>
	                <include>*.jar</include>
	            </includes>
	        </fileSet>
	    </fileSets>
	</assembly>

## 鸣谢
* 华哥，在讲解maven合理划分模块后，也给予了打包部署的思路。

