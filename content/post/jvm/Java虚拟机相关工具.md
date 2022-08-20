---
title: "虚拟机相关工具"
date: 2022-08-20T09:40:53+08:00
draft: false
categories: ["JVM"]
tags: ["java","jvm"]
---

本文主要是为了介绍虚拟机相关的工具，包括故障处理、性能监控和一些其他工具。
## 故障处理工具
|   名称             | 全称 | 作用及描述        | 
| ----- | ----------------------------- |----|
|  `jps`     | JVM Process Status Tool | 显示指定系统内所有的HotSpot虚拟机进程    |
|  `jstat`   | JVM Statistics Monitoring Tool | 用于收集HotSpot虚拟机各方面运行数据    |
|  `jinfo`   | Configuration Info for Java | 显示虚拟机配置信息   |
|  `jmap`   | Memory Map for Java | 生成虚拟机的内存快照（heapdump文件）   |
|  `jhat`   | JVM Heap Dump Browser | 用于分析heapdump文件，会建立一个http/html服务器，让用户可以在浏览器查看分析结果   |
|  `jstack`   | Stack Trace for Java |  显示虚拟机的线程快照   |

### jps
类似Linux上的ps命令（查看进程信息的），jps是用来查看Java进程信息的。 （LVMID，Local Virtual Machine Identifier）
示例：
```
mango@mangodeMacBook-Pro ~ % jps -lmv
388  -Xms750m -Xmx750m -Xmn400m -XX:MetaspaceSize=248m -XX:MaxMetaspaceSize=500m -XX:+PrintGCDetails -Xloggc://Users/mango/logs/ideagc.log -verbose:gc -Xverify:none -XX:+DisableExplicitGC -XX:+UnlockCommercialFeatures -XX:+FlightRecorder -XX:ReservedCodeCacheSize=240m -XX:+UseG1GC -XX:SoftRefLRUPolicyMSPerMB=50 -ea -XX:CICompilerCount=2 -Dsun.io.useCanonPrefixCache=false -Djava.net.preferIPv4Stack=true -Djdk.http.auth.tunneling.disabledSchemes="" -XX:+HeapDumpOnOutOfMemoryError -XX:-OmitStackTraceInFastThrow -Djdk.attach.allowAttachSelf=true -Dkotlinx.coroutines.debug=off -Djdk.module.illegalAccess.silent=true -XX:+UseCompressedOops -Dfile.encoding=UTF-8 -XX:ErrorFile=/Users/mango/java_error_in_idea_%p.log -XX:HeapDumpPath=/Users/mango/java_error_in_idea.hprof -Djb.vmOptionsFile=/Users/mango/Library/Preferences/IdeaIC2019.3/idea.vmoptions -Didea.paths.selector=IdeaIC2019.3 -Didea.executable=idea -Didea.platform.prefix=Idea -Didea.home.path=/Applications/IntelliJ IDEA CE.app/Contents
7095 sun.tools.jps.Jps -lmv -Dapplication.home=/Library/Java/JavaVirtualMachines/jdk1.8.0_221.jdk/Contents/Home -Xms8m
``` 
参数：
```
-q 只输出LVMID，省略主类名称
-m 输出main()函数的参数
-l 输出启动类路径
-v 输出虚拟机启动时的JVM参数
```
### jstat
 可以显示本地或者远程虚拟机进程中的类加载、内存、垃圾收集、即时编译等运行时数据信息。
示例：
```
mango@mangodeMacBook-Pro ~ % jstat -class 388
Loaded  Bytes  Unloaded  Bytes     Time
 36365 73094.0        0     0.0      66.21
```
参数：
![](/mb/images/jvm2/tool/01.png)
### jinfo
作用是实时查看和调整虚拟机各项参数。
使用：
```
Usage:
    jinfo <option> <pid>
       (to connect to a running process)

where <option> is one of:
    -flag <name>         to print the value of the named VM flag
    -flag [+|-]<name>    to enable or disable the named VM flag
    -flag <name>=<value> to set the named VM flag to the given value
    -flags               to print VM flags
    -sysprops            to print Java system properties
    <no option>          to print both VM flags and system properties
    -? | -h | --help | -help to print this help message
```
### jmap
用于生成堆转储快照。
使用方式：
```
Usage:
    jmap [option] <pid>
        (to connect to running process)
    jmap [option] <executable <core>
        (to connect to a core file)
    jmap [option] [server_id@]<remote server IP or hostname>
        (to connect to remote debug server)
```
示例：
```
mango@mangodeMacBook-Pro ~ % jmap -dump:format=b,file=idea.bin 7166
Dumping heap to /Users/mango/idea.bin ...
Heap dump file created
```
### jhat
与jmap搭配使用，来分析jmap生成的堆转储快照。
示例：
```
mango@mangodeMacBook-Pro ~ % jhat idea.bin
Reading from idea.bin...
Dump file created Fri Aug 19 16:24:22 CST 2022
Snapshot read, resolving...
Resolving 7657475 objects...
Chasing references, expect 1531 dots...........................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
Eliminating duplicate references...........................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
Snapshot resolved.
Started HTTP server on port 7000
Server is ready.
```
通过http://localhost:7000来访问内存分析结果。
![](/mb/images/jvm2/tool/02.png)
### jstack
用于生成虚拟机当前时刻的线程快照(一般称为threaddump或者 javacore文件)。
参数：
```
-F 当正常输出的请求不被响应时，强制输出线程堆栈
-l 除堆栈外，显示关于锁的附加信息
-m 如果调用到本地方法的话，可以显示C/C++的堆栈
```
示例：(输出结果只截取了部分）
```
mango@mangodeMacBook-Pro ~ % jstack -l 7369
2022-08-19 16:34:01
Full thread dump OpenJDK 64-Bit Server VM (11.0.6+8-b520.66 mixed mode):

Threads class SMR info:
_java_thread_list=0x0000600001f8a2a0, length=45, elements={
0x00007f858f1c2000, 0x00007f858f1ef800, 0x00007f858f200000, 0x00007f858f20c000,
0x00007f8590034800, 0x00007f8590035000, 0x00007f8590038000, 0x00007f858f208000,
0x00007f858f24b000, 0x00007f8590809000, 0x00007f85900a6000, 0x00007f8590018000,
0x00007f8590949000, 0x00007f858f255000, 0x00007f858f8c5000, 0x00007f858f8d3000,
0x00007f85901d7000, 0x00007f85909a6800, 0x00007f85909c4000, 0x00007f8590264800,
0x00007f8590268800, 0x00007f85909ed000, 0x00007f858f3ed800, 0x00007f858f476000,
0x00007f858f4db800, 0x00007f858f4d9800, 0x00007f8590be5000, 0x00007f8590c4b800,
0x00007f85902b4000, 0x00007f858f5c5800, 0x00007f858faa1000, 0x00007f8590dca800,
0x00007f85900e9800, 0x00007f85903a8000, 0x00007f85903b8000, 0x00007f859587a000,
0x00007f8595197000, 0x00007f859528d800, 0x00007f859528a000, 0x00007f858f2b0800,
0x00007f8590732000, 0x00007f8595aed800, 0x00007f85909d6000, 0x00007f8596845000,
0x00007f8599821000
}

"Reference Handler" #2 daemon prio=10 os_prio=31 cpu=6.70ms elapsed=32.36s tid=0x00007f858f1c2000 nid=0x3f03 waiting on condition  [0x0000700010280000]
   java.lang.Thread.State: RUNNABLE
	at java.lang.ref.Reference.waitForReferencePendingList(java.base@11.0.6/Native Method)
	at java.lang.ref.Reference.processPendingReferences(java.base@11.0.6/Reference.java:241)
	at java.lang.ref.Reference$ReferenceHandler.run(java.base@11.0.6/Reference.java:213)

   Locked ownable synchronizers:
	- None

"Finalizer" #3 daemon prio=8 os_prio=31 cpu=2.67ms elapsed=32.36s tid=0x00007f858f1ef800 nid=0x4403 in Object.wait()  [0x0000700010383000]
   java.lang.Thread.State: WAITING (on object monitor)
	at java.lang.Object.wait(java.base@11.0.6/Native Method)
	- waiting on <no object reference available>
	at java.lang.ref.ReferenceQueue.remove(java.base@11.0.6/ReferenceQueue.java:155)
	- waiting to re-lock in wait() <0x00000007d3e7a738> (a java.lang.ref.ReferenceQueue$Lock)
	at java.lang.ref.ReferenceQueue.remove(java.base@11.0.6/ReferenceQueue.java:176)
	at java.lang.ref.Finalizer$FinalizerThread.run(java.base@11.0.6/Finalizer.java:170)

   Locked ownable synchronizers:
	- None

"Signal Dispatcher" #4 daemon prio=9 os_prio=31 cpu=0.30ms elapsed=32.34s tid=0x00007f858f200000 nid=0x4203 runnable  [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

   Locked ownable synchronizers:
	- None
```

## 性能监控工具
|   名称             | 全称 | 作用及描述        | 
| ----- | ----------------------------- |----|
|  `JHSDB`     |  | 是一款基于服务性代理（Serviceability Agent,SA)实现的进程外调试工具。    |
|  `JConsole`     | Java Monitoring and Management Console | 是一款基于JMX的可视化监控管理工具。  |
|  `VisualVM`     | All-in-One Java Troubleshooting Tool | 多合一故障处理工具，支持插件，及运行监视、故障处理、性能分析于一身  |
|  `JMC`     | Java Mission Control |  JMC与虚拟机采用JMX协议通信，可以作为JMX控制台，也作为JFR分析工具  |
### JHSDB
笔者如果是在Mac的机器上，可参考[HSDB 在mac下的启动和使用](https://www.jianshu.com/p/9a26e85a2482)打开HSDB工具。
使用如下命令打开HSDB:
```
sudo java -cp /Library/Java/JavaVirtualMachines/jdk1.8.0_221.jdk/Contents/Home/lib/sa-jdi.jar sun.jvm.hotspot.HSDB
```
运行截图如下：（具体功能，感兴趣的可以自己研究一下）
![](/mb/images/jvm2/tool/03.png)
### JConsle
是一款基于JMX的可视化管理工具。
直接双击JDK目录下的`jconsole`命令行启动(在oracle jdk1.8的bin目录下有)：
![](/mb/images/jvm2/tool/04.png)
可以查看内存、线程、类加载、虚拟机参数及MBean相关信息。
### VisualVM
是一款多功能工具，支持插件扩展。
直接双击JDK目录下的`jvisualvm`命令行启动(在oracle jdk1.8的bin目录下有)，也可以独立下载对应软件：
![](/mb/images/jvm2/tool/05.png)
其中有个Visual GC的插件推荐使用，可以图形化看到内存垃圾回收相关信息。
### Java Mission Control
除了做JMX控制台外，还能做为JFR分析工具。
直接双击JDK目录下的`jcm`命令行启动(在oracle jdk1.8的bin目录下有)，也可以独立下载对应软件：
![](/mb/images/jvm2/tool/06.png)

其中MBean（MBean就是被[JMX管理](https://baike.baidu.com/item/JMX/2829357?fr=aladdin)的资源）在JConsle、VisualVM和JMC中都可以查看。
JMX(Java管理扩展)提供了一种简单的、基础的方法，用来管理诸如应用、设备和服务等资源。

## 其他工具
|   名称             | 全称 | 作用及描述        | 
| ----- | ----------------------------- |----|
|  `HSDIS`     | HotSpot disassembler  | 一个Sun官方推荐的HotSpot虚拟机JIT编译代码的反汇编插件    |
|  `JITWatch`     |  | JIT编译分析工具，配合HSDIS能查看Java源码、字节码和汇编码的对应关系。  |

详细使用请参考：[Java反汇编：HSDIS、JITWatch](https://zhuanlan.zhihu.com/p/158168592)


## 参考资料
* 周志明 * 《深入理解Java虚拟机》
* Mac下使用JHSDB https://www.jianshu.com/p/9a26e85a2482
