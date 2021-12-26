---
title: java之深入jvm之路
date: 2019-12-14 14:45:07
categories: ["技术文章"]
tags: ["java","jdk","jvm","gc"]
draft: false
---
# 1.仔细看一看java
## 1.1.java发展历史
![](/mb/images/jvm/java-develop-time.png)
* 1995年5月23 Oak语言更名为Java
* 1996年1月23 JDK 1.0发布
* 1997年2月19日JDK 1.1发布

    > 技术代表：JDBC，JAR文件格式，JavaBeans，RMI。
* 1998年12月4日里程碑版本 JDK1.2
  
    > 技术体系拆分为面向桌面级应用开发的J2SE、面向企业级应用开发的J2EE、面向手机等移动端开发的J2ME；这本版本的 Java虚拟机第一内置了JIT（编译器）。
* 1999年4月27HotSpot虚拟机发布
  
    > HotSpot最初是一家小公司开发，由于其优秀的 表现，这家公司在1997年被sun公司收购，HotSpot虚拟机发布时是作为Java1.2的附加程序提供的，后来它成为了JDK1.3以及之后的所有版本的Sun JDK的默认虚拟机。
* 2004年9月30日  JDK1.5发布
  
    > 工程代号Tiger，在语法易用性上做了很大的改进，例如：自动装箱，泛型，枚举，可变参数，遍历循环（foreach循环）等。
* 2006年12月11日 JDK1.6发布
  
    > 启用Java SE6，Java 6EE，Java ME6的命名方式，提供动态语言支持，提供编译API，微型HTT服务器API；同时这个版本对Java虚拟机内部做了大量改进，包括锁与同步、垃圾收集、类加载等方面的算法都有很大的改动。
* 2006年11月13日 Sun公司宣布Java开源，建立OpenJDK组织对代码进行管理
* 2009年12月，SUN公司发布Java EE 6
* 2011年7月28日，Oracle公司发布Java SE 7
* 2014年3月18日，Oracle公司发表Java SE 8(市场主流版本)
* 2017年9月21日，Oracle公司发表Java SE 9

## 1.2.java体系结构
![](/mb/images/jvm/jdk-art.jpg)
# 2.仔细看一看jvm
## 2.1.jvm是什么
<img src="/mb/images/jvm/jvm-art.png" width="700px">

## 2.2.类加载（class loader）
### 2.2.1.类加载
当程序主动使用某个类时，如果该类还未被加载到内存中，则JVM会通过加载、连接、初始化3个步骤来对该类进行初始化。
![](/mb/images/jvm/class-load.jpeg)
（***加载 -> 链接（验证-准备-解析） -> 初始化 -> 使用 -> 卸载*** 等生命周期）

类加载指的是将类的`class`文件读入到内存，并为之创建一个`java.lang.Class`对象，也就是说，当程序中使用任何类时，系统都会为之建立一个`java.lang.Class`对象（会存放在方法区中）。

类的加载由`类加载器`完成，`类加载器`通常由JVM提供，这些类加载器也是前面所有程序运行的基础，JVM提供的这些类加载器通常被称为`系统类加载器`。除此之外，开发者可以通过继承`ClassLoader`基类来创建自己的类加载器。
#### 2.2.1.1.加载
将***某处***的`class字节码`读入到JVM内存中，得到`class`的***二进制流***
JVM规范中并没有限制class的二进制流从何处来，因此出现了如下技术：
* zip/jar/ear/war
* 网络
* 动态代理
* 应用生成，例如jsp
* ...

#### 2.2.1.2.链接
JVM拿到字节码二进制流后，会进过链接步骤，链接包含验证、准备和解析。
* 验证
    > 文件格式验证、元数据验证、字节码验证、符号引用验证。
    流是不是以`0xCAFFBABE`开头，（明确知道是正规的`class`集合时可以使用`-Xverify:none`关闭验证）
* 准备
  
    > 为类的变量(`static`修饰的)分配内存（方法区）及初始值，执行类代码块如`static{}`代码块
* 解析
    > 常量池里的***符号引用***替换为***直接引用***。

    > 符号引用：符号引用是以一组符号来描述所引用的目标，符号可以是任何的字面形式的字面量，只要不会出现冲突能够定位到就行。布局和内存无关。

    > 直接引用：是指向目标的指针，偏移量或者能够直接定位的句柄。该引用是和内存中的布局有关的，并且一定加载进来的。

### 2.2.2.类加载器

#### 2.2.2.1.定义

虚拟机设计团队把类加载阶段中的

> 通过一个类的全限定名来获取描述此类的二进制字节流

的这个动作放到Java虚拟机外部去实现，以便让应用程序自己决定如何去获取所需要的类。

实现这个动作的代码模块就是`类加载器`。

#### 2.2.2.2.三大类加载器

![](/mb/images/jvm/classloader.png)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

* 启动类加载器（`Bootstrap ClassLoader`）

> 是嵌在JVM内核中的加载器，该加载器是用C++语言写的，主要负载加载`JAVA_HOME/lib`下的类库，启动类加载器无法被应用程序直接使用。

* 扩展类加载器（`Extension ClassLoader`）

> 该加载器器是用JAVA编写，且它的父类加载器是`Bootstrap ClassLoader`，是由`sun.misc.Launcher$ExtClassLoader`实现的，主要加载`JAVA_HOME/lib/ext`目录中的类库。开发者可以选择使用扩展类加载器。

* 应用程序类加载器（`Application ClassLoader`）

> 系统类加载器，也称为应用程序类加载器，负责加载应用程序`classpath`目录下的所有`jar`和`class`文件。它的父加载器为`Ext ClassLoader`。  

#### 2.2.2.3.双亲委派模型       

<img src="/mb/images/jvm/dobule-parent.jpg" width="500px"> 

如果一个类加载器收到了一个类加载请求，它不会自己去尝试加载这个类，而是把这个请求转交给父类加载器去完成。每一个层次的类加载器都是如此。因此所有的类加载请求都应该传递到最顶层的启动类加载器中，只有到父类加载器反馈自己无法完成这个加载请求（在它的搜索范围没有找到这个类）时，子类加载器才会尝试自己去加载。

<font color="red"> 委派能确保一个类只被加载一次。</font>

双亲委派模型很好地解决了各个类加载器的基础类统一问题(越基础的类由越上层的加载器进行加载)，基础类之所以被称为“基础”，是因为它们总是作为被调用代码调用的API。

``` java
protected synchronized Class<?> loadClass(String paramString, boolean paramBoolean)
  throws ClassNotFoundException
{
  //检查是否被加载过
  Class localClass = findLoadedClass(paramString);
  //如果没有加载，则调用父类加载器
  if (localClass == null) {
    try {
      //父类加载器不为空
      if (this.parent != null)
        localClass = this.parent.loadClass(paramString, false);
      else {
        //父类加载器为空，则使用启动类加载器
        localClass = findBootstrapClass0(paramString);
      }
    }
    catch (ClassNotFoundException localClassNotFoundException)
    {
      //如果父类加载失败，则使用自己的findClass方法进行加载
      localClass = findClass(paramString);
    }
  }
  if (paramBoolean) {
    resolveClass(localClass);
  }
  return localClass;
}
```

#### 2.2.2.4.破坏双亲委派模型

参考资料：

1. [JDBC、Tomcat为什么要破坏双亲委派模型？](https://www.cnblogs.com/yueshutong/p/11430885.html)
2. [聊聊JDBC是如何破坏双亲委派模型的]( https://www.jianshu.com/p/60dbd8009c64)

> 如果基础类，要调用用户类的代码？ 例如JNDI,JDBC,JCE,JAXB和JBI等。
>
> Java中所有涉及SPI的加载动作基本上都采用`线程上下文件类加载器(Thread Context ClassLoader)`(这个类加载器可以通过`java.lang.Thread`类的`setContextClassLoader()`方法进行设置。

* 用户强制复写`loadClass()`，即可打破双亲委派模型。不推荐，建议复写`findClass()`。
* 看看JDBC如何实现的？

##### 2.2.2.4.1.JDBC如何破坏双亲委派模型

> 首先，理解一下为什么JDBC需要破坏双亲委派模式，原因是原生的JDBC中Driver驱动本身只是一个接口，并没有具体的实现，具体的实现是由不同数据库类型去实现的。例如，MySQL的mysql-connector-*.jar中的Driver类具体实现的。 原生的JDBC中的类是放在rt.jar包的，是由启动类加载器进行类加载的，在JDBC中的Driver类中需要动态去加载不同数据库类型的Driver类，而mysql-connector-*.jar中的Driver类是用户自己写的代码，那启动类加载器肯定是不能进行加载的，既然是自己编写的代码，那就需要由应用程序启动类去进行类加载。于是乎，这个时候就引入线程上下文件类加载器(Thread Context ClassLoader)。有了这个东西之后，程序就可以把原本需要由启动类加载器进行加载的类，由应用程序类加载器去进行加载了。

``` java
	private static Connection getConnection(
        String url, java.util.Properties info, Class<?> caller) throws SQLException {
        /*
         * When callerCl is null, we should check the application's
         * (which is invoking this class indirectly)
         * classloader, so that the JDBC driver class outside rt.jar
         * can be loaded from here.
         */
        //callerCL为空的时候，其实说明这个ClassLoader是启动类加载器，但是这个启动类加载并不能识别rt.jar之外的类，这个时候就把callerCL赋值为Thread.currentThread().getContextClassLoader();也就是应用程序启动类
        ClassLoader callerCL = caller != null ? caller.getClassLoader() : null;
        synchronized(DriverManager.class) {
            // synchronize loading of the correct classloader.
            if (callerCL == null) {
                callerCL = Thread.currentThread().getContextClassLoader();
            }
        }

        if(url == null) {
            throw new SQLException("The url cannot be null", "08001");
        }

        println("DriverManager.getConnection(\"" + url + "\")");

        // Walk through the loaded registeredDrivers attempting to make a connection.
        // Remember the first exception that gets raised so we can reraise it.
        SQLException reason = null;

        for(DriverInfo aDriver : registeredDrivers) {
            // If the caller does not have permission to load the driver then
            // skip it.
            //继续看这里 
            if(isDriverAllowed(aDriver.driver, callerCL)) {
                try {
                    println("    trying " + aDriver.driver.getClass().getName());
                    Connection con = aDriver.driver.connect(url, info);
                    if (con != null) {
                        // Success!
                        println("getConnection returning " + aDriver.driver.getClass().getName());
                        return (con);
                    }
                } catch (SQLException ex) {
                    if (reason == null) {
                        reason = ex;
                    }
                }

            } else {
                println("    skipping: " + aDriver.getClass().getName());
            }

        }

        // if we got here nobody could connect.
        if (reason != null)    {
            println("getConnection failed: " + reason);
            throw reason;
        }

        println("getConnection: no suitable driver found for "+ url);
        throw new SQLException("No suitable driver found for "+ url, "08001");
    }

    private static boolean isDriverAllowed(Driver driver, ClassLoader classLoader) {
        boolean result = false;
        if(driver != null) {
            Class<?> aClass = null;
            try {
                //这一步会对类进行初始化的动作，而初始化之前自然也要进行的类的加载工作
                aClass =  Class.forName(driver.getClass().getName(), true, classLoader);
            } catch (Exception ex) {
                result = false;
            }

             result = ( aClass == driver.getClass() ) ? true : false;
        }

        return result;
    }
```

##### 2.2.2.4.2.TOMCAT如何破坏双亲委派模型

Tomcat如何破坏双亲委派模型的呢？

**每个Tomcat的webappClassLoader加载自己的目录下的class文件，不会传递给父类加载器。**

<img src="/mb/images/jvm/tomcat-classloader.png" width="500px"> 

事实上，tomcat之所以造了一堆自己的classloader，大致是出于下面三类目的：

- 对于各个 `webapp`中的 `class`和 `lib`，需要相互隔离，不能出现一个应用中加载的类库会影响另一个应用的情况，而对于许多应用，需要有共享的lib以便不浪费资源。
- 与 `jvm`一样的安全性问题。使用单独的 `classloader`去装载 `tomcat`自身的类库，以免其他恶意或无意的破坏；
- 热部署。相信大家一定为 `tomcat`修改文件不用重启就自动重新装载类库而惊叹吧。

## 2.3.运行时数据区（runtime data area)

jvm运行时数据区主要包含 方法区、运行时常量池、栈、本地方法栈、程序计数器、堆、直接内存等。

<img src="/mb/images/jvm/jvm-rda.png" width="600px">

### 2.3.1.方法区(method area)

方法区和堆一样，是各个线程共享内存区域，用来存放已被加载类信息、常量、静态变量、即时编译器编译后的代码等数据。

在jdk1.7中，被称为“永久代”（Permanent Generation）；

在jdk1.8中，被称为“元数据”(Matadata)。

### 2.3.2.运行时常量池（Runtime Constant Pool）

运行时常量池是方法区中的一部分。Class文件中除了有类的版本、字段、方法、接口等描述信息外，还有一项信息是常量池（Constant Pool Table)，用于存放编译期生成的各种**字面量**和 **符号引用** ，这部分内容将在类加载后进入方法区的运行时常量池中存放。

`String.intern()` 请参考 https://www.cnblogs.com/naliyixin/p/8984077.html

> 采用new 创建的字符串对象不进入字符串池，直接用静态字符串的操作的会添加到字符串池。
>
> 在定义变量的时候赋值，如果赋值的是静态的字符串，就会执行进入字符串池的操作，如果池中含有该字符串，则返回引用。

### 2.3.3.jvm栈(jvm stack) 

jvm栈，又称Java虚拟机栈，是**线程私有**的，它的生命周期与线程相同。

jvm栈描述的是Java方法执行的内存模型：每个Java方法在执行的时候都会创建一个栈帧（Stack Frame)，用于存储局部变量表、操作数栈、动态链接、方法出口等信息。每一个方法从调用直至执行完成的过程，就对应着一个栈帧在虚拟机栈中入栈到出栈的过程。

#### 2.3.3.1.栈帧(Stack Frame)

* 局部变量表：存放方法参数、局部变量；

* 操作数栈： 存放执行字节码指令，如iadd等， 更多请参考 https://www.cnblogs.com/kexianting/p/8523296.html

* 动态链接： 存放符号引用，运行时才确定是直接引用，支持多态特性。
* 方法出口：存放返回地址（returnAddress类型，指向一条字节码地址的指令）。

#### 2.3.3.2.StackOverflowError和OutOfMemoryError异常

这个区域定义了2个异常：

* 如果线程请求的栈深度大于虚拟机所允许的深度，将抛出StackOverflowError异常。（大部分虚拟机可动态扩展）

* 如果线程请求的栈无法申请到足够的内存，就会抛出OutOfMemoryError异常。

### 2.3.4.本地方法栈(native method stack)

本地方法栈和虚拟机栈类似，也是**线程私有**的，区别在于虚拟机栈用于执行Java方法（字节码）服务；而本地方法栈用于执行虚拟机使用到的Native方法服务。在虚拟机规范中对本地方法栈中方法使用的语言，使用方式与数据结构并没有强制规定，因此具体的虚拟机可以自由实现它。

有的虚拟机（比如Sun HotSpot虚拟机）直接把本地方法栈和虚拟机栈合并。

想了解更多关于Java本地方法，请参考 https://blog.csdn.net/lansine2005/article/details/5753741

``` java
public class IHaveNatives
    {
      native public void Native1( int x ) ;
      native static public long Native2() ;
      native synchronized private float Native3( Object o ) ;
      native void Native4( int[] ary ) throws Exception ;
    } 

// java.system.loadLibrary()加载dll库，在调用本地方法时
```



### 2.3.5.程序计数器(program counter register)

程序计数器是一块较小的内存空间，可以看做是当前线程所执行的字节码行号指示器。

字节码解释器工作时就是通过改变计数器的值来选取吓一跳需要执行的字节码指令，分支、循环、跳转、异常处理、线程恢复(cpu)、线程切换(cpu)等基础功能都需要依赖程序计数器来完成。

为了线程切换后能恢复到正确的执行位置，每条线程都需要一个独立的程序计数器，各个线程之间计数器互补影响，独立存储，所以程序计数器也是**线程私有**的内存。

### 2.3.6.堆（heap）

Java堆是Java虚拟机中所管理内存最大的一块，是被所有线程共享的一块内存区域，在虚拟机启动时创建。Java堆是GC（垃圾回收）管理的主要区域，因此很多时候被叫做GC堆。

几乎所有对象都要在Java堆上分配。（随着JIT编译器的发展和逃逸技术成熟，所有对象都分配在堆上就没那么绝对了）

从内存回收角度，分代收集算法，可分为 新生代和老年代，更细可分为Eden区、From Survivor区、To Survivor区和老年区。从内存分配角度，线程共享的Java堆中可能划分出多个线程私有的分配缓存区（Thread Local Allocation Buffer,TLAB）。

Java程序可通过`-Xmx`和`-Xms`等参数配置堆内存的大小。更多jvm参数，请参考 https://www.cnblogs.com/shoshana-kong/p/10559186.html

### 2.3.7.直接内存（Direct Memory）

直接内存并不是虚拟机运行时数据区的一部分，也不是Java虚拟机规范中定义的内存区域。但这部分内存被频繁使用，也会导致OOM异常。

在JDK1.4中加入了NIO，引入了一种基于通道（Channel）与缓冲区（Buffer）的IO方式，它可以使用Native函数库直接分配堆外内存，然后通过一个存储在Java堆中的DirectByteBuffer对象作为这块内存的引用进行操作。（在一些缓存场景显著提高性能，因为避免了Java堆和Native堆中来回复制数据）

## 2.4.执行子系统(execution engine) 


# 3.仔细看一看GC
## 3.1.什么是垃圾回收

在C语言、C++语言中，可以通过malloc和free来主动申请内存和释放内存，程序的内存是由开发者自己管理的。但是这样有个缺点，就是很多程序容易出现内存泄漏的问题。所以在Java语言中，Java设计者引入了垃圾回收机制，由Java虚拟机来自动完成内存回收，清除掉已经不再使用的对象，释放内存空间。

## 3.2.如何定位垃圾

可以添加`-XX:+PrintGCDetails`配置，打印GC日志来分析垃圾回收过程。

### 3.2.1.引用计数算法(reference-counting)

每个对象都有一个引用计数器，当对象被引用一次，计数器就加1，当对象引用失效一次就减1，当计数器为0，意味着对象是垃圾对象，可以被GC回收。**循环引用的对象无法被判断为垃圾**

### 3.2.2.可达性算法(GC Root Tracing)

![](/mb/images/jvm/gc-root.png)

从GC Root作为起点开始搜索，那么整个连通图中对象都是活的，对于GC Root无法达到的对象便是垃圾对象，随时可被GC回收。

采用引用计数算法的系统只需在每个实例对象创建之初，通过计数器来记录所有的引用次数即可。而可达性算法，则需要再次GC时，遍历整个GC根节点来判断是否回收。

Java中的对象都链接在一个个根节点上，所以内存中会有许多的根节点（即GC Roots），内存回收的时候最费时间的就是找到这些根节点。Java虚拟机中有一种表OopMap记录了部分根节点和对象的链接关系，通过它可以进行**枚举根节点**。但在程序运行的过程中一直都有对象的创建，消亡，所以该表一直都在变化，所以必须在某个时刻更新表，这个时间点称为**安全点（safe point）**。根据表找到对象的根节点，通过引用链找到该对象判断它是否GC可达。

#### 3.2.2.1.GC Root存放的对象

（1）虚拟机栈中的引用对象
（2）方法去中静态属性引用的对象
（3）方法区中常量引用的对象
（4）本地方法栈native方法引用的对象

#### 3.2.2.2.缺陷

1. 耗时长：找到根节点以及在大量数据中逐个检查引用耗费大量时间。
2. GC停顿：安全点问题，这个时间点会导致Java所有执行线程的停顿。

#### 3.2.2.3.算法优化

1. **枚举根节点**：在类加载完成时就将根节点和对象的链接关系写入到OopMap中，后续查询直接查OopMap。
2. **安全点**：因为程序运行过程中，会有对象创建，消亡，所以OopMap一直在变化。于是需要在某个时刻更新OopMap，这个时间点就是安全点。安全点的时候回Stop The World。
3. **安全区域**：由于Java程序大部分是多线程的，所以在某个安全点时，会有线程（sleep/blocked)无法到达安全点的情况，于是拓宽安全点为安全区域。

## 3.3.垃圾回收算法

### 3.3.1.标记-清除（Mark-Sweep）

<img src="/mb/images/jvm/gc-mark-sweep.jpg" width="600px">

先标记内存空间中的对象是否是垃圾，然后再清除掉。

缺点：

1. 内存碎片
2. 效率低
3. 单线程会stw

### 3.3.2.复制（Copying)

<img src="/mb/images/jvm/gc-copying.jpg" width="600px">

将内存空间划分为2块相等的空间，每次只用一块；下一次将存活的对象copy到另外一个部分，然后清除掉原来使用的部分。

缺点：内存空间缩小一半，**该算法应用在新生代的Surivior区**。

### 3.3.3.标记整理（Mark-Compact）

<img src="/mb/images/jvm/gc-mark-compact.jpg" width="600px">

为了解决Copying算法的缺陷，充分利用内存空间，提出了Mark-Compact算法。该算法标记阶段和Mark-Sweep一样，但是在完成标记之后，它不是直接清理可回收对象，而是将存活对象都向一端移动，然后清理掉端边界以外的内存。

缺点：效率低，**该算法应用在老年代**。

## 3.4.分代收集算法

<img src="/mb/images/jvm/gc-generation.png" width="800px">

分代收集算法其实是一种理论，不是实际的算法。是将堆按年龄分代分区域，主要分为年轻代和老年代；年轻代分为Eden区和Surivior区，Surivior区分为Form和To2个区域。

1. 年轻代 ： 老年代 = 1 ：2
2. Eden区 ： Form区 ： To区 = 8 ：1：1
3. 年轻代里的对象存活15次后将进入老年代
4. 如果对象内存大于S区一半，将直接进入老年代

## 3.5.常见的GC回收器

垃圾回收器是内存回收的具体实现，常见的垃圾回收器如下图。

<img src="/mb/images/jvm/gc-list.png" width="600px">

**新生代收集器**：Serial、ParNew、Parallel Scavenge

**老年代收集器**：CMS、Serial Old、Parallel Old

**整堆收集器**： G1

了解几个概念：

**并行收集**：指多条垃圾收集线程并行工作，但此时用户线程仍处于等待状态。

**并发收集**：指用户线程与垃圾收集线程同时工作（不一定是并行的可能会交替执行）。用户程序在继续运行，而垃圾收集程序运行在另一个CPU上。

**吞吐量**：即CPU用于运行用户代码的时间与CPU总消耗时间的比值（吞吐量 = 运行用户代码时间 / ( 运行用户代码时间 + 垃圾收集时间 )）。例如：虚拟机共运行100分钟，垃圾收集器花掉1分钟，那么吞吐量就是99%

常用的垃圾收集器：

1. Serial收集器： 单线程，串行；使用`-XX:+UseSerialGC`配置开启；Serial收集器使用在新生代，是JDK1.3.1之前虚拟机的新生代垃圾收集的唯一选择；Serial Old收集器使用在老年代。
2. ParNew收集器：多线程，使用`-XX:+UseParNewGC`配置开启，使用`-XX:ParalleGCThread=4`来设置线程数，应用在新生代。
3. Parallel Scavenge收集器：多线程，并行；带有自适应调节策略；应用在新生代；使用多线程和标记-整理算法。
4. Serial Old收集器：单线程，串行；是Serial在老年代的实现版本。
5. Parallel Old收集器： 多线程，并行；是Parallel在老年代的实现版本。
6. CMS收集器： 使用标记-清除算法；并发收集，低停顿。应用在老年代。
7. G1收集器：并行收集，并发收集；分代收集；空间整合；可预测停顿；使用`-XX:+UseG1GC`配置开启。整堆区域收集。

详细请参考 https://www.cnblogs.com/chenpt/p/9803298.html

### 3.5.1.jdk各版本默认垃圾回收器

| jdk版本     | 新生代            | 老年代       |
| ----------- | ----------------- | ------------ |
| 1.6,1.7,1.8 | Parallel Scavenge | Parallel Old |
| 1.9         | G1                | G1           |

