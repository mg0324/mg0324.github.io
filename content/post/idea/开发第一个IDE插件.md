---
title: "开发第一个IDE插件"
date: 2022-01-22T22:45:27+08:00
draft: false
categories: ["技术文章","idea"]
tags: ["idea","idea plugin"]
---

## 前言
问：为什么要开发idea插件呢？

答：你一定用过很多idea插件，比如`ideaVim`,`Maven`,`lombok`,`markdown`等。

|  ![](/mb/images/idea/first/01.png)   |  ![](/mb/images/idea/first/02.png)   |
| --- | --- |
|  ![](/mb/images/idea/first/03.png)   |  ![](/mb/images/idea/first/04.png)   |

这些都是插件，安装后你的idea就能获得对应的能力。

现在想象你是一个插件开发者，通过开发插件来增强idea的能力，并发布到idea的插件仓库，分享给其他人。这样是不是很有意思呢！

## 环境信息
* 操作系统： macOs catalina 10.15.7
* idea版本：2021.3.1 社区版
* jdk版本：jdk-11.0.14.jdk

![](/mb/images/idea/first/05.png)

## 开发第一个插件
### 新建plugin项目
选择左侧`IntelliJ Platform Plugin`，并设置SDK，点击下一步；
![](/mb/images/idea/first/06.png)
填写项目名称，并设置项目所在路径，点finish。
![](/mb/images/idea/first/07.png)

### 插件工程简介
![](/mb/images/idea/first/08.png)
* 依赖IntelliJ IDEA SDK
* 在`resources/META-INF`下的`plugin.xml`是插件的配置文件，很重要，也是插件运行入口

### plugin.xml介绍及内容
~~~
<idea-plugin>
  <!-- 插件ID，全世界唯一 -->
  <id>com.mango.idea.hello.ide.id</id>
  <!-- 插件名称，会显示在插件详情页 -->
  <name>mango hello ide</name>
  <!-- 插件版本 -->
  <version>1.0</version>
  <!-- 插件联系人，网址 -->
  <vendor email="1092017732@qq.com" url="http://mg.meiflower.top">mango mei</vendor>
  <!-- 插件描述，会显示在插件详情页 -->
  <description><![CDATA[
      mango mei first ide plugin.<br>
      hello world,you can study it
    ]]></description>
  <!-- 插件更新日志，会显示在插件详情页 -->
  <change-notes><![CDATA[
      1.0 version<br>
    ]]>
  </change-notes>

  <!-- idea版本检查，至少173.0以上 -->
  <idea-version since-build="173.0"/>

  <!-- 请查看 https://plugins.jetbrains.com/docs/intellij/plugin-compatibility.html 插件依赖能力 -->
  <depends>com.intellij.modules.platform</depends>

  <extensions defaultExtensionNs="com.intellij">
    <!-- 在这里添加你的扩展 -->
  </extensions>

  <actions>
    <!-- 在这里添加你的action -->
  </actions>

</idea-plugin>
~~~
### 创建action
添加Hello动作到邮件菜单
![](/mb/images/idea/first/09.png)
点击完成会自动生成如下配置到`plugin.xml`：
~~~
<actions>
  <!-- 在这里添加你的action -->
  <action id="mangoHello" class="com.mango.idea.hello.HelloAction" text="Hello" description="Hello IDE">
    <add-to-group group-id="EditorPopupMenu" anchor="first"/>
    <keyboard-shortcut keymap="$default" first-keystroke="ctrl meta J"/>
  </action>
</actions>
~~~

### HelloAction逻辑
点击弹出提示`Hello IDE`
~~~
public class HelloAction extends AnAction {

    @Override
    public void actionPerformed(AnActionEvent e) {
        Notifications.Bus.notifyAndHide(new Notification(new String("MangoTip"),"Hello Title","Hello IDE", NotificationType.INFORMATION));
    }
}
~~~
### 运行调试
![](/mb/images/idea/first/10.png)
![](/mb/images/idea/first/11.png)
![](/mb/images/idea/first/12.png)

## 打包插件
点击下图编译打包动作
![](/mb/images/idea/first/13.png)
就会生成如下jar包
![](/mb/images/idea/first/14.png)

## 发布插件
* 1.发布到idea在线仓库，需要先注册 https://plugins.jetbrains.com/
* 2.然后通过如下入口上传插件，审核通过后才能在插件市场内搜索到
![](/mb/images/idea/first/15.png)
![](/mb/images/idea/first/16.png)

或者另外一种方式，直接把打包好的jar包copy给朋友，拖拽到idea内就能安装了。


