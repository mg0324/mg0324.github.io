---
title: "千呼万唤始出来的IDEA笔记插件mdNote"
date: 2022-03-01T18:28:39+08:00
draft: false
categories: ["技术文章","idea"]
tags: ["idea","idea plugin","md"]
---

## 前言
最近工作上在做IDEA插件开发的东西，所以需要深入学习。在网上看到一个比较好的例子，实现一个笔记插件，故实现后发布这篇博客，分享给同样在学习的你。

（mdNote插件下载地址：https://mangomei.lanzouy.com/iWLPb00tn8vc）
更多细节及实现欢迎下载源码学习：https://gitee.com/mgang/idea-demo/tree/master/md-note

其实也可以按[第一个IDEA插件hello ide开发](%E7%AC%AC%E4%B8%80%E4%B8%AAIDEA%E6%8F%92%E4%BB%B6helloide%E5%BC%80%E5%8F%91.md)里提到的发布插件的方式，发布到官网插件仓库。
## 环境信息

![](/mb/images/idea/md-note/01.png) 

（小插曲：之前下载的是最新版的idea ce版2021.3.1，出现插件中文4横线中文乱码问题。所以换成2019.3.5版本，没有上述中文乱码问题。）

## 主要功能列表及知识点
1. 提供一个视窗，展示要保存的笔记数据（视窗开发）
2. 选中文件内的文本右键能加入到笔记数据（右键action及弹窗）
3. 点击保存md按钮后，生成对应的md笔记（文件选择器及模板渲染）

## 实现步骤详细
### 建立视窗并注册
通过视窗工厂创建视窗内容，其中`MdNoteUI`是通过`GUI Form`的方式创建（布局和逻辑分离）

![](/mb/images/idea/md-note/02.png) 

``` java
/**
 * md note 视窗提供者
 */
public class MdNoteWindowFactory implements ToolWindowFactory {

    @Override
    public void createToolWindowContent(@NotNull Project project, @NotNull ToolWindow toolWindow) {
        // 从toolWindow获取contentManager
        ContentManager contentManager = toolWindow.getContentManager();
        // 从contentManager获取contentFactory
        ContentFactory contentFactory = contentManager.getFactory();
        // contentFactory创建内容
        MdNoteUI mdNoteUI = new MdNoteUI(project);
        Content content = contentFactory.createContent(mdNoteUI.view(),"main",true);
        // 将内容通过contentManager注册到视窗
        contentManager.addContent(content);
    }
}
```
并注册到扩展点上。
~~~
<extensions defaultExtensionNs="com.intellij">
  <!-- Add your extensions here -->
  <toolWindow factoryClass="com.mango.idea.md.note.window.MdNoteWindowFactory" id="MdNote" anchor="right"></toolWindow>
</extensions>
~~~
### 视窗内容设计
按如下布局设计内容

![](/mb/images/idea/md-note/03.png) 

### 选择文本并右击保持到笔记
新建action注册到右键菜单`EditorPopupMenu`,取名为`add md note`。
~~~
<action id="mp-add-note-note" class="com.mango.idea.md.note.action.AddMdNoteAction"
        text="add md note" description="add md note">
  <add-to-group group-id="EditorPopupMenu" anchor="first"/>
  <keyboard-shortcut keymap="$default" first-keystroke="shift ctrl meta M"/>
</action>
~~~
在选择文本后点击`add md note`，弹出标题和描述对话框。
~~~
/**
 * 添加md note action
 */
public class AddMdNoteAction extends AnAction {

    @Override
    public void actionPerformed(AnActionEvent e) {
        // 获取鼠标选中的文本
        String selectedText = e.getRequiredData(CommonDataKeys.EDITOR).getSelectionModel().getSelectedText();
        // 获取当前右键的文件名
        VirtualFile virtualFile = e.getData(PlatformDataKeys.VIRTUAL_FILE);
        String fileName =  virtualFile.getName();
        // 显示弹框，填写标题和描述
        AddNoteDialog addNoteDialog = new AddNoteDialog(selectedText,fileName);
        addNoteDialog.showAndGet();
    }
}
~~~

![](/mb/images/idea/md-note/04.png) 

![](/mb/images/idea/md-note/05.png) 

确定后，视窗就能正常显示出笔记。
### 点击保存到md保存笔记
输入笔记标题，并点击保存到md

![](/mb/images/idea/md-note/06.png) 

最后预览一下生成的笔记。（使用freemarker做模板生成）

![](/mb/images/idea/md-note/07.png) 

## 总结
* 学习到如何开发设计一个视窗
* 学习到如何获取鼠标选中的文本
* 学习到如何使用`GUI form`的方式做布局
* 学习到`JTable`做数据展示及清除
* 学习到如何使用`FileChooser`做文件路径选择

更多细节及实现欢迎下载源码学习：https://gitee.com/mgang/idea-demo/tree/master/md-note