---
title: "熟悉Java类文件class结构"
date: 2022-09-01T00:27:48+08:00
draft: false
categories: ["JVM"]
tags: ["java","jvm"]
---

Java基于Class文件作为存储格式，不同平台对应虚拟机实现的方式让Java具备跨平台的特性。
因此我们有必要更深入学习Class字节码文件的结构。
## Class文件的结构
Class文件是一组以8个字节为基础单位的二进制流，采用一种类似于C语言结构体的伪结构来存储数据（可以看做是一张表），这种伪结构中只有两种数据类型:
* 无符号数：基本数据类型，以u1,u2,u4,u8分别表示1个字节、2个字节、4个字节和8个字节的无符号数； 无符号数可以用来描述数字、索引引用、数量值或者按照UTF-8编码构成字符串值。
* 表：表是由多个无符号数或者其他数据项组成的复合数据项，命名以`_info`为后缀。

***注意：各个数据项按顺序依次排列，没有空隙，省空间***

class文件按照顺序各数据项内容如下表所示：

|  数据项            |  类型   |   名称                                |   数量   |
| ---------------- | ------- | ----------------------------- | -------- |
| 魔数                |  u4     |  magic                                |  1         |
| 次版本号         |  u2     |  minor_version                   |  1         |
| 主版本号         |  u2     |  major_version                   |  1         |
| 常量池计数      |  u2     |  constant_pool_count        |  1         |
| 常量池表集合  |  `cp_info`     |  constant_pool         |  constant_pool_count - 1        |
| 访问标志        |  u2     |  access_flags                      |  1         |
| 类索引           |  u2     |  this_class                           |  1         |
| 父类索引         |  u2     |  super_class                      |  1         |
| 接口计数         |  u2     |  interfaces_count               |  1         |
| 接口索引集合  |  u2     |  interfaces                          |  interfaces_count         |
| 字段计数         |  u2     |  fields_count                      |  1         |
| 字段表集合      |  `field_info`     |  fields                     |  fields_count         |
| 方法计数         |  u2     |  methods_count                 |  1         |
| 方法表集合      |  `method_info`     |  methods          |  methods_count         |
| 属性计数         |  u2     | attributes_count                 |  1         |
| 属性表集合      |  `attribute_info`     |  attributes        |  attributes_count         |

其中有`cp_info`、`field_info`、`method_info`和`attribute_info`4个表类型，其他均为无符号数。
温馨提示：IDEA内可以使用`jclasslib`插件查看Class文件内容。

![](/mb/images/jvm2/class-struct/01.png)

## 魔数及版本
|  数据项            |  类型   |   名称                                |   数量   |
| ---------------- | ------- | ----------------------------- | -------- |
| 魔数                |  u4     |  magic                                |  1         |
| 次版本号         |  u2     |  minor_version                   |  1         |
| 主版本号         |  u2     |  major_version                   |  1         |
* 前4个字节存的是魔术，值为`CAFEBABE`。（咖啡宝贝）
***注意：下图是以16进制查看的，一个16进制位=4个2进制位，则2个16进制位=8个2进制位=1个字节。那么魔术的4哥字节就是8个16进制位，正好是CAFEBABE。***

![](/mb/images/jvm2/class-struct/02.png)

* 2个字节的次版本号，`0x0000`=0。

![](/mb/images/jvm2/class-struct/03.png)

* 2个字节的主版本号，`0x0034`=16x3+4=52，对应1.8版本。

![](/mb/images/jvm2/class-struct/04.png)

如下图是class文件版本号说明：

![](/mb/images/jvm2/class-struct/05.png)

## 常量池
|  数据项            |  类型   |   名称                                |   数量   |
| ---------------- | ------- | ----------------------------- | -------- |
| 常量池计数      |  u2     |  constant_pool_count        |  1         |
| 常量池表集合  |  `cp_info`     |  constant_pool         |  constant_pool_count - 1        |
* Class文件里的资源仓库。
* 常量池的计数是从1开始的，0号索引用来表示“不引用任何一个常量池”。
* 常量池中主要存放**字面量**和**符号引用**，其中字面量接近Java语言层面的常量概念，如文本字符串、被声明为final的常量值等；而符号引用则属于编译原理方面的概念，主要包括如下几类常量：
    *  被模块导出或者开放的包(Package)  
    * 类和接口的全限定名(Fully Qualified Name)  
    * 字段的名称和描述符(Descriptor)  
    * 方法的名称和描述符  
    * 方法句柄和方法类型(Method Handle、Method Type、Invoke Dynamic) 
    * 动态调用点和动态常量(Dynamically-Computed Call Site、Dynamically-Computed Constant)
* 当虚拟机做类加载时，将从常量池中获取符号引号，再在类创建时或运行时解析翻译到具体的内存地址之中。（C和C++的链接过程是将方法和字段翻译并得到内存布局信息，是静态编译。而Java语言是在类加载时通过获取类文件中的常量池符号引号后翻译到具体内存地址的，是动态编译。）
* 常量池中每一项都是一个表，最初有11种基础类型，后面增加了4种类型支持动态语言调用，再后面又增加了2种类型支持模块化，截止到Java 13，常量池中共17种类型常量。

![](/mb/images/jvm2/class-struct/06.png)

* 以上17种类型常量，每个类型都有自己的数据项，具体细节请查阅《深入理解Java虚拟机》的第6.3节。如下图列出各种类型的数据项：

![](/mb/images/jvm2/class-struct/07.png)
![](/mb/images/jvm2/class-struct/08.png)
![](/mb/images/jvm2/class-struct/09.png)
![](/mb/images/jvm2/class-struct/10.png)

## 访问标志
|  数据项            |  类型   |   名称                                |   数量   |
| ---------------- | ------- | ----------------------------- | -------- |
| 访问标志        |  u2     |  access_flags                      |  1         |
常量池结束之后，紧接着2个字节表示访问标志（类的），记录如下标志信息：

![](/mb/images/jvm2/class-struct/11.png)

## 类索引、父类索引和接口索引集合
|  数据项            |  类型   |   名称                                |   数量   |
| ---------------- | ------- | ----------------------------- | -------- |
| 类索引           |  u2     |  this_class                           |  1         |
| 父类索引         |  u2     |  super_class                      |  1         |
| 接口计数         |  u2     |  interfaces_count               |  1         |
| 接口索引集合  |  u2     |  interfaces                          |  interfaces_count         |

访问标志之后，类索引和父类索引都是一个u2的类型的数据，而接口索引集合是一个u2类型的集合，这3项定义了类的继承关系。

![](/mb/images/jvm2/class-struct/12.png)
![](/mb/images/jvm2/class-struct/13.png)

## 字段表集合
|  数据项            |  类型   |   名称                                |   数量   |
| ---------------- | ------- | ----------------------------- | -------- |
| 字段计数         |  u2     |  fields_count                      |  1         |
| 字段表集合      |  `field_info`     |  fields                     |  fields_count         |

接口索引集合后是字段表，字段表用于描述接口或类中声明的变量。

变量信息有：
* 访问标识，public、private和protected
* 是否静态，static
* 是否常量，final
* 是否具备并发可见性，volatile
* 是否需要序列化，transient
* 变量类型，是基本类型，还是对象类型，还是数组类型

字段表结构如下图：

![](/mb/images/jvm2/class-struct/14.png)

其中访问标识是一个u2类型数据，值如下图：

![](/mb/images/jvm2/class-struct/15.png)

如下图是一个例子：

![](/mb/images/jvm2/class-struct/16.png)

可以看出字段表中只有一个字段，就是logger，其访问标识是0x0000，是未指定，在Java中默认是private。
`name_index`和`descriptor_index`都是u2类型数据，分别表示字段的简单名称和描述符，存的是常量池的索引。
几个概念：
* 全限定名：`com/github/mg0324/mango/card/StartupApplication；`把类的全路径中的点替换为/，不要.class后缀，最后以;结尾。
* 简单名称：指没有类型和参数修饰的方法或者变量名称，如`add()`方法和`logger`变量的简单名称分别为`add`和`logger`。
* 描述符：用来描述字段的数据类型、方法的参数列表（包括数量、类型以及顺序）和返回值。如下图是描述符标识字符和类型对应说明。

![](/mb/images/jvm2/class-struct/17.png)

如果定义一个`java.lang.String[][]`，则描述符为`[[java.lang.String;`;如果定义一个`int[]`，则描述符为`[I`。

## 方法表集合
|  数据项            |  类型   |   名称                                |   数量   |
| ---------------- | ------- | ----------------------------- | -------- |
| 方法计数         |  u2     |  methods_count                 |  1         |
| 方法表集合      |  `method_info`     |  methods          |  methods_count         |

字段表之后，就是方法表。
方法表的数据类型和字段表类似，依次是访问标志（`access_flags`）、简单名称(`name_iindex`)、方法描述符(`descriptor_index`)、属性计数(`attributes_count`)和方法属性表（`attributes`)。

![](/mb/images/jvm2/class-struct/18.png)

方法和字段相比，不能用`final`和`transient`修饰，但多了`synchronized`、`native`、`abstract`和`staticfp`可修饰，因此访问标志也随之变化，如下图：

![](/mb/images/jvm2/class-struct/19.png)

而方法里面的代码则是通过属性表中的`Code`属性来存储的，方法的参数是通过属性表中的`MethodParameters`属性来存储的。如下图例子：

![](/mb/images/jvm2/class-struct/20.png)

如果父类方法在子类中没有被重载，则方法集合中不会出现父类的方法。
但同样地有可能会出现编译器自动增加的方法，如类初始化`<clint>`方法和实例初始化`<init>`方法。

## 属性表集合
|  数据项            |  类型   |   名称                                |   数量   |
| ---------------- | ------- | ----------------------------- | -------- |
| 属性计数         |  u2     | attributes_count                 |  1         |
| 属性表集合      |  `attribute_info`     |  attributes        |  attributes_count         |

方法表之后，就是属性表。

* Class文件、字段表、方法表都可以携带自己的属性表集合，以描述某些场景专有的信息。
* 《Java虚拟机规范》Java SE 12中定义了29种属性需要虚拟机实现。

![](/mb/images/jvm2/class-struct/21.png)
![](/mb/images/jvm2/class-struct/22.png)
![](/mb/images/jvm2/class-struct/23.png)

其中，每一项属性的详细细节，请查阅《深入理解Java虚拟机》的第6.3.7节。

## 参考资料
* 周志明 * 《深入理解Java虚拟机》