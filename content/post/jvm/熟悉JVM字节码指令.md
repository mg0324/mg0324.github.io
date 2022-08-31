---
title: "熟悉JVM字节码指令"
date: 2022-09-01T00:19:31+08:00
draft: false
categories: ["JVM"]
tags: ["java","jvm"]
---

## 简介
* Java虚拟机的指令由一个字节长度（256个操作码）的、代表着特定操作含义的数字（`操作码，Opcode`）和跟随其后的零至多个代表其操作需要的参数（`操作数，Operand`）构成。
* 由于Java虚拟机采用面向操作数栈的架构，所以大部分指令都只有一个操作码，操作数都是放到操作数栈中。
* 如果不考虑异常，则简单的指令执行模型的伪代码如下：
``` 伪代码
do {  
    自动计算PC寄存器的值加1; 
    根据PC寄存器指示的位置，从字节码流中取出操作码;
     if (字节码存在操作数) {
        从字节码流中取出操作数; 
    }
    执行操作码所定义的操作;
} while (字节码流长度 > 0);
```
## 字节码与数据类型
* 在Java虚拟机指令集中，大多少指令都包含其操作的数据类型信息。
* 对于大部分与数据类型相关的指令，它们的操作码助记符中都有特殊字符来专门表明该指令服务的数据类型：i代表对int类型的数据操作
    * i代表int
    * l代表long
    * s代表short
    * b代表byte
    * c代表char
    * f代表 float
    * d代表double
    * a代表reference
* 如下图是Java虚拟机指令集所支持的数据类型：**（其中操作码如iadd，是操作码助记符）**

![](/mb/images/jvm2/class-code/01.png)

## 加载和存储指令
加载和存储指令用于将数据在栈帧中的局部变量表和操作数栈之间来回传输。
这类指令包括：
* 将一个局部变量加载到操作数栈：iload、iload_\<n>、lload、lload_\<n>、fload、fload_\<n>、dload、dload_\<n>、aload、aload_\<n>
* 将一个数值从操作数栈存储到局部变量表：istore、istore_\<n>、lstore、lstore_\<n>、fstore、fstore_\<n>、dstore、dstore_\<n>、astore、astore_\<n>
* 将一个常量加载到操作数栈：bipush、sipush、ldc、ldc_w、ldc2_w、aconst_null、iconst_m1、iconst_\<i>、lconst_\<l>、fconst_\<f>、dconst_\<d>
* 扩充局部变量表访问索引的指令：wide

## 运算指令
运算指令用于对2个操作数栈上的值进行特定操作，并将结果重新存入操作数栈顶。
所有运算指令包括：
* 加法指令：iadd、ladd、fadd、dadd
* 减法指令：isub、lsub、fsub、dsub
* 乘法指令：imul、lmul、fmul、dmul
* 除法指令：idiv、ldiv、fdiv、ddiv
* 求余指令：irem、lrem、frem、drem
* 取反指令：ineg、lneg、fneg、dneg
* 位移指令：ishl、ishr、iushr、lshl、lshr、lushr
* 按位或指令：ior、lor
* 按位与指令：iand、land
* 按位异或指令：ixor、lxor
* 局部变量自增指令：iinc
* 比较指令：dcmpg、dcmpl、fcmpg、fcmpl、lcmp

## 类型转换指令
类型转换指令可以将2种不同数组类型相互转换。
* Java虚拟机直接支持数值宽泛类型转换，即小范围向大范围转换。（安全的，不会丢失精度：如int到long、float或者double；long到float或者double；float到double）
* 窄化类型转换（可能会发生上限溢出、下限溢出和精度丢失等情况），需要用户显示类型转换，指令包括：
    * i2b - int转换为byte
    * i2c - int转换为char
    * i2s - int转换为short
    * l2i - long转换为int
    * f2i - float转换为int
    * f2l - float转换为long
    * d2i - double转换为int
    * d2l - double转换为long
    * d2f - double转换为float
## 对象创建与访问指令
Java虚拟机对对象和数组采用了不同的指令，对象创建后，就可以使用对象访问指令来获取对象或者数组中的字段或者数组元素。这些指令包括：
* 创建类实例的指令：new
* 创建类数组的指令：newarray、anewarray、mutilanewarray
* 访问类字段指令：getstatic、putstatic
* 访问实例字段指令：getfield、putfield
* 把一个数组元素加载到操作数栈的指令：baload、caload、saload、iaload、laload、faload、daload、aaload
* 将一个操作数栈中的值储存到数组元素中的指令：bastore、castore、sastore、iastore、lastore、fastore、dastore、aastore
* 取数组长度的指令：arraylength
* 检查类实例类型的指令：instanceof、checkcast

## 操作数栈管理指令
如同操作一个普通数据结构栈的一样，Java虚拟机提供了一些操作操作数栈的指令，包括：
* 将操作数栈顶的一个或者2个元素出栈：pop、pop2
* 复制栈顶一个或2个数值，并将复制值或双份复制值重新压入到栈顶：dup、dup2、dup_x1、dup2_x1、dup_x2、dup2_x2
* 将栈最顶端的2个数值交换：swap

## 控制转移指令
控制转移指令可以让Java虚拟机有条件或无条件的从指定位置的下一条指令继续执行程序。（概念模型上理解其实就是修改PC寄存器的值）
指令包括：
* 条件分支指令：ifeq、iflt、ifle、ifgt、ifge、ifnull、ifnotnull、if_icmpeq、ificmpne、ificmplt、ificmpgt、ificmple、ificmpge、ifacmpeq和ifacmpne
* 复合条件分支指令：tableswitch、lookupswitch
* 无条件分支：goto、goto_w、jsr、jsr_w、ret

## 方法调用和返回指令
方法调用的5条指令：
* invokevirtual指令：用于调用对象的实力方法。
* invokeinterface指令：用于调用接口方法，它会在运行时搜索一个实现了这个接口方法的对象，找出合适的方法进行调用。
* invokespecial指令：用于调用一些需要特殊处理实例方法，包括实例初始化方法、私有方法和父类方法。
* invokestatic指令：用于调用类静态方法。
* invokedynamic指令：用于在运行时动态解析出调用点限定符所引用的方法，并执行该方法。

前面4条调用指令的分派逻辑都固化在虚拟机内部，用户无法改变，而invokedynamic指令的分派逻辑是有用户所设定的引导方法决定的。

方法调用指令与数据类型无关，而返回指令则与数据类型相关，包括：
* ireturn指令：返回值是boolean、byte、char、short和int类型时使用。
* lreturn指令：返回值是long
* freturn指令：返回值是float
* dreturn指令：返回值是double
* areturn指令：返回值是对象
* return指令：返回值为void

## 异常处理指令
* athrow指令：显示抛出异常指令。
* 自动抛出异常，如1/0时会抛出 `ArithmeticException`异常。
*  在Java虚拟机中，处理异常(cat ch语句)不是由字节码指令来实现的(很久之前曾经使用jsr和 ret指令来实现，现在已经不用了)，而是采用异常表来完成。

## 同步指令
Java虚拟机可以支持方法级同步和一段指令序列的同步，这两种同步结构的实现都是使用管程（monitor，锁）来实现的。
* 方法级的同步是隐式的，无需通过字节码指令实现。虚拟机可以从类文件的方法表结构种的ACC_SYNCHRONIZED访问标志得知一个方法是不是同步方法。当方法被调用时，如果被设置了同步方法则需要先获取管程（锁），才能执行方法，执行完成后释放管程（锁）。
* 同步一段指令序列，则是由synchronized对应的monitorenter和monitorexit这2条字节码指令实现的。

![](/mb/images/jvm2/class-code/02.png)

**编译器会自动产生一个异常处理程序（上图中红框对应的字节码序列），这个异常处理程序声明可处理所有的异常，它的目的就是用来执行monitorexit指令。**

## 参考资料
* 周志明 * 《深入理解Java虚拟机》



