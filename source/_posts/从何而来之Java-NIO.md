---
title: 从何而来之Java NIO
date: 2021-10-13 22:29:37
categories: java
tags: 
- java
- NIO
---

2021-10-02 周六
## 缘起
最近在看《Java NIO》这本书，书中详细讲解了`jdk1.4`内提供的关于实现`nio`的`API`。因为阅读后，发现对于NIO还是学习的不够深入，之前也仅仅是学习了Java的文件IO和Socket编程，再者也是用`Netty`框架编写NIO代码，并未用Java提供的NIO实践。借此机会，把Java关于网络IO的发展给整理清楚，并编写Java代码示例，加深理解！！！
IO其实分为文件IO和流IO，这里讨论的是流IO，也就是Socket的IO。
## 图解Java网络IO发展历程

<img src="/mb/images/javanio/history.png">

* 1996年1月发布`jdk1.0`版本，支持Java BIO的`Socket`编程。
* *2001年1月`Linux`内核发布2.4版本，支持NIO，非阻塞IO。*
* 2002年2月发布`jdk1.4`版本，支持Java NIO的`SocketChannel`编程，支持非阻塞。
* 2011年7月发布`jdk1.7`版本，支持Java AIO的`AsynchronousServerSocketChannel`编程。

## Java实现BIO（阻塞）
<img src="/mb/images/javanio/bio-show.png">
### SocketServerDemo 服务端
``` java
package org.mango.demo.bio;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * 1连接1线程模型（线程资源有限，不适用）
 * 将连进来的连接交给新的线程处理，这样主线程负责处理客户端连接，工作线程处理连接数据读取和写入
 * 支持客户端多连接
 * @Description socket server 编写的bio服务端 jdk1.0
 * @Date 2021-10-02 15:19
 * @Created by mango
 */
public class SocketServerDemo {
    public static void main(String[] args) throws IOException {
        // jdk1.0 版本，基于ServerSocket
        ServerSocket serverSocket = new ServerSocket();
        int port = 9000;
        serverSocket.bind(new InetSocketAddress(port));
        System.out.println("server listen on port " + port);
        while (true) {
            // 调用accept()方法，会阻塞
            Socket socket = serverSocket.accept();
            System.out.println(socket + " connect success!!");
            // 将连进来的连接交给新的线程处理，这样主线程负责处理客户端连接，工作线程处理连接数据读取和写入
            // 支持客户端多连接
            new WorkThread(socket).start();
        }
    }
}

/**
 * 工作线程
 */
class WorkThread extends Thread{
    private Socket socket;
    public WorkThread(Socket socket){
        this.socket = socket;
    }
    @Override
    public void run() {
        String tn = Thread.currentThread().getName();
        String sn = socket.toString();
        // 将接收到的数据后跟 处理线程名称 发送给客户端
        boolean loop = true;
        while(loop){
            try {
                DataInputStream dis = new DataInputStream(socket.getInputStream());
                DataOutputStream dos = new DataOutputStream(socket.getOutputStream());
                // 从inputStream流读取数据，会阻塞
                String data = dis.readUTF();
                System.out.println(tn + ":" + sn + " receive data:" + data);
                String rData = data + ":" +tn;
                dos.writeUTF(rData);
            } catch (IOException e) {
                // 连接异常关闭，线程结束
                try {
                    socket.close();
                    loop = false;
                    System.out.println(tn + ":" + sn + " exception close!");
                } catch (IOException e1) {
                    e1.printStackTrace();
                }
            }
        }
    }
}
/**
 * 执行结果：
 * server listen on port 9000
 * Socket[addr=/127.0.0.1,port=60357,localport=9000] connect success!!
 * Socket[addr=/127.0.0.1,port=60387,localport=9000] connect success!!
 * Thread-0:Socket[addr=/127.0.0.1,port=60357,localport=9000] receive data:你好
 * Thread-1:Socket[addr=/127.0.0.1,port=60387,localport=9000] receive data:中国
 * Thread-0:Socket[addr=/127.0.0.1,port=60357,localport=9000] exception close!
 * Thread-1:Socket[addr=/127.0.0.1,port=60387,localport=9000] exception close!
 */
```
执行结果打印：
``` java
 server listen on port 9000
 Socket[addr=/127.0.0.1,port=60357,localport=9000] connect success!!
 Socket[addr=/127.0.0.1,port=60387,localport=9000] connect success!!
 Thread-0:Socket[addr=/127.0.0.1,port=60357,localport=9000] receive data:你好
 Thread-1:Socket[addr=/127.0.0.1,port=60387,localport=9000] receive data:中国
 Thread-0:Socket[addr=/127.0.0.1,port=60357,localport=9000] exception close!
 Thread-1:Socket[addr=/127.0.0.1,port=60387,localport=9000] exception close!
```

### SocketClientDemo 客户端
``` java
package org.mango.demo.bio;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.util.Scanner;

/**
 * @Description TODO
 * @Date 2021-10-02 23:15
 * @Created by mango
 */
public class SocketClientDemo {
    public static void main(String[] args) throws IOException {
        Socket socket = new Socket();
        // 连接服务端
        String host = "127.0.0.1";
        int port = 9000;
        socket.connect(new InetSocketAddress(host,port));
        System.out.println("connect server " + host + ":" + port + " success!");

        // 接收命令
        Scanner scanner = new Scanner(System.in);
        System.out.println("输入exit:客户端退出；其他为发送数据!");
        // 发送数据
        DataOutputStream dos = new DataOutputStream(socket.getOutputStream());
        DataInputStream dis = new DataInputStream(socket.getInputStream());
        boolean loop = true;
        while(loop) {
            System.out.print("请输入：");
            String input = scanner.next();
            if("exit".equals(input)){
                socket.close();
                loop = false;
            }else{
                dos.writeUTF(input);
                System.out.println("send success,data:" + input);
                // 等待服务端发送数据,readUTF 方法会阻塞
                String sData = dis.readUTF();
                System.out.println("receive data:" + sData);
            }
        }
        System.out.println("client exit!");
    }
}

执行结果打印：
``` java
 执行结果1:
 connect server 127.0.0.1:9000 success!
 输入exit:客户端退出；其他为发送数据!
 请输入：你好
 send success,data:你好
 receive data:你好:Thread-0
 请输入：exit
 client exit!
```
``` java
 执行结果2:
 connect server 127.0.0.1:9000 success!
 输入exit:客户端退出；其他为发送数据!
 请输入：中国
 send success,data:中国
 receive data:中国:Thread-1
 请输入：exit
 client exit!
```

***总结：***
***1. Socket默认就是阻塞的，并不支持设置非阻塞。***
***2. accept() 和 从流读取数据的read() 都是阻塞的。***

## Java实现NIO
### 单线程版本
`NonBlockServerDemo` - 服务端
``` java
package org.mango.demo.nio;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

/**
 * @Description （服务端非阻塞）主动遍历 一个线程处理客服端连接，数据读取
 * @Date 2021-10-01 15:26
 * @Created by mango
 */
public class NonBlockServerDemo {
    public static void main(String[] args) throws IOException, InterruptedException {
        // 存放连接进来的SocketChannel
        List<SocketChannel> scList = new ArrayList<>();
        // 服务端，使用ServerSocketChannel
        ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
        int port = 9000;
        // 绑定本地端口
        serverSocketChannel.bind(new InetSocketAddress(port));
        System.out.println("server listen on " + port);
        // 设置服务端通道非阻塞
        serverSocketChannel.configureBlocking(false);

        while (true){
            // accept方法非阻塞，立即返回，null表示没有client连接进来
            SocketChannel sc = serverSocketChannel.accept();
            if(null == sc){
                Thread.sleep(200);
            }else{
                System.out.println(Thread.currentThread().getName() + " client enter " + sc.toString());
                // 设置连接非阻塞
                sc.configureBlocking(false);
                // 维护到集合中
                scList.add(sc);
            }
            // 遍历连接，读取数据
            for(SocketChannel temp : scList){
                // 创建一个缓存区
                ByteBuffer buffer = ByteBuffer.allocate(1 * 1024);
                // read方法非阻塞，返回值为数据长度
                int len = temp.read(buffer);
                String socketName = temp.toString();
                if(len > 0){
                    System.out.println(Thread.currentThread().getName() + " " + socketName + " receive data size is " + len);
                    ByteBuffer data = ByteBuffer.allocate(len);
                    // 翻转缓冲区，使得能被put
                    buffer.flip();
                    data.put(buffer);
                    System.out.println(Thread.currentThread().getName() + " " + socketName + " receive data is " + new String(data.array(), StandardCharsets.UTF_8));
                }
            }
        }
    }
}
```
执行结果：
``` java
 /**
 * 执行结果：
 * server listen on 9000
 * main client enter java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:50039]
 * main java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:50039] receive data size is 3
 * main java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:50039] receive data is 123
 * main java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:50039] receive data size is 6
 * main java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:50039] receive data is 你好
 * main java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:50039] receive data size is 6
 * main java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:50039] receive data is 中国
 * main client enter java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:50308]
 * main java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:50308] receive data size is 3
 * main java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:50308] receive data is 123
 * main java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:50308] receive data size is 3
 * main java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:50308] receive data is xxx
 * main java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:50039] receive data size is 4
 * main java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:50039] receive data is exit
 * main java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:50308] receive data size is 4
 * main java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:50308] receive data is exit
 */
```
`NonBlockClientDemo` - 客户端
``` java
package org.mango.demo.nio;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

/**
 * @Description 非阻塞测试 客户端
 * @Date 2021-10-01 15:48
 * @Created by mango
 */
public class NonBlockClientDemo {
    public static void main(String[] args) throws IOException {
        SocketChannel sc = SocketChannel.open();
        String host = "127.0.0.1";
        int port = 9000;
        boolean isConnect = sc.connect(new InetSocketAddress(host,port));
        if(isConnect){
            System.out.println("connect server " + host + ":" + port + " success!");
            // 从输入流中读取数据
            Scanner scanner = new Scanner(System.in);
            System.out.println("输入exit:客户端退出；其他为发送数据!");
            boolean loop = true;
            while (loop){
                System.out.print("请输入:");
                String input = scanner.next();
                ByteBuffer data = ByteBuffer.wrap(input.getBytes(StandardCharsets.UTF_8));
                // 发送数据
                sc.write(data);
                if("exit".equals(input)){
                    loop = false;

                }
            }
        }
        System.out.println("client exit!");
    }
}
```
执行结果：
``` java
/**
 * 执行结果1：
 * connect server 127.0.0.1:9000 success!
 * 输入exit:客户端退出；其他为发送数据!
 * 请输入:123
 * 请输入:你好
 * 请输入:中国
 * 请输入:exit
 * client exit!
 */
```
``` java
/**
 * 执行结果2：
 * connect server 127.0.0.1:9000 success!
 * 输入exit:客户端退出；其他为发送数据!
 * 请输入:123
 * 请输入:xxx
 * 请输入:exit
 * client exit!
 */
```
### 多线程版本

`MTNonBlockServerDemo` - 服务端
``` java
package org.mango.demo.mtnio;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.nio.charset.StandardCharsets;

/**
 * @Description （服务端非阻塞）主动遍历 一线程1连接，数据读取
 * @Date 2021-10-01 15:26
 * @Created by mango
 */
public class MTNonBlockServerDemo {
    public static void main(String[] args) throws IOException, InterruptedException {
        // 服务端，使用ServerSocketChannel
        ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
        int port = 9000;
        // 绑定本地端口
        serverSocketChannel.bind(new InetSocketAddress(port));
        System.out.println("server listen on " + port);
        // 设置服务端通道非阻塞
        serverSocketChannel.configureBlocking(false);

        while (true){
            // accept方法非阻塞，立即返回，null表示没有client连接进来
            SocketChannel sc = serverSocketChannel.accept();
            if(null == sc){
                Thread.sleep(200);
            }else{
                System.out.println(Thread.currentThread().getName() + " client enter " + sc.toString());
                // 设置连接非阻塞
                sc.configureBlocking(false);
                new WorkThread(sc).start();
            }
        }
    }
}
/**
 * 工作线程
 */
class WorkThread extends Thread{
    private SocketChannel socketChannel;
    public WorkThread(SocketChannel socketChannel){
        this.socketChannel = socketChannel;
    }
    @Override
    public void run() {
        boolean loop = true;
        String tn = Thread.currentThread().getName();
        String sn = socketChannel.toString();
        try{
            // 将接收到的数据后跟 处理线程名称 发送给客户端
            while(loop){
                ByteBuffer buffer = ByteBuffer.allocate(1024);
                // read() 不会阻塞
                int len = socketChannel.read(buffer);
                if(len > 0) {
                    System.out.println(tn + ":" + sn + " receive data size :" + len);
                    ByteBuffer data = ByteBuffer.allocate(len);
                    // 翻转缓冲区，使得能被put
                    buffer.flip();
                    data.put(buffer);
                    String sData = new String(data.array(),StandardCharsets.UTF_8);
                    System.out.println(tn + ":" + sn + " receive data:" + sData);
                    String rData = sData + ":" + tn;
                    socketChannel.write(ByteBuffer.wrap(rData.getBytes(StandardCharsets.UTF_8)));
                }
            }
        } catch (IOException e) {
            // 异常退出
            try {
                socketChannel.close();
            } catch (IOException e1) {
                e1.printStackTrace();
            }
            System.out.println(tn + ":" + sn + " exception close!");
        }
    }
}
```
``` java
/**
 * 执行结果：
 * server listen on 9000
 * main client enter java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:54386]
 * Thread-0:java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:54386] receive data size :3
 * Thread-0:java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:54386] receive data:123
 * Thread-0:java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:54386] receive data size :6
 * Thread-0:java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:54386] receive data:你好
 * main client enter java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:54480]
 * Thread-1:java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:54480] receive data size :6
 * Thread-1:java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:54480] receive data:中国
 * Thread-1:java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:54480] receive data size :3
 * Thread-1:java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:54480] receive data:123
 * Thread-1:java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:54480] receive data size :4
 * Thread-1:java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:54480] receive data:exit
 * Thread-1:java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:54480] exception close!
 * Thread-0:java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:54386] receive data size :4
 * Thread-0:java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:54386] receive data:exit
 * Thread-0:java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:54386] exception close!
 */
```
`MTNonBlockClientDemo` - 客户端
``` java
package org.mango.demo.mtnio;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

/**
 * @Date 2021-10-03 15:26
 * @Created by mango
 */
public class MTNonBlockClientDemo {
    public static void main(String[] args) throws IOException, InterruptedException {
        SocketChannel sc = SocketChannel.open();
        String host = "127.0.0.1";
        int port = 9000;
        sc.connect(new InetSocketAddress(host,port));
        // 设置非阻塞
        sc.configureBlocking(false);
        System.out.println("connect server " + host + ":" + port + " success!");
        // 从输入流中读取数据
        Scanner scanner = new Scanner(System.in);
        System.out.println("输入exit:客户端退出；其他为发送数据!");
        boolean loop = true;
        while (loop){
            System.out.print("请输入:");
            String input = scanner.next();
            ByteBuffer data = ByteBuffer.wrap(input.getBytes(StandardCharsets.UTF_8));
            // 发送数据
            sc.write(data);
            if("exit".equals(input)){
                loop = false;
            }
        }
        System.out.println("client exit");
    }
}
```
执行结果：
``` java
/**
 * 执行结果1：
 * connect server 127.0.0.1:9000 success!
 * 输入exit:客户端退出；其他为发送数据!
 * 请输入:123
 * 请输入:你好
 * 请输入:exit
 * client exit
 */
```
``` java
/**
 * 执行结果2：
 * connect server 127.0.0.1:9000 success!
 * 输入exit:客户端退出；其他为发送数据!
 * 请输入:中国
 * 请输入:123
 * 请输入:exit
 * client exit
 */
```
***总结：***
***1. 通过channel的configureBlocking(flase)设置连接为非阻塞后，accept()或者read()方法就会直接返回***
***2. 1连接1线程虽然能提高服务端处理客户端并发连接数，但是线程资源有限，不易多开。因此多线程版本再优化就可以放到线程池管理。***
***3. 将线程用线程池管理起来，就能改为线程池版本非阻塞IO模型。***
``` java 
// 创建工作线程池
ExecutorService executorService = Executors.newFixedThreadPool(8);
// 提交到线程池
executorService.submit(new WorkThread(sc));
```
### 多路复用器版本
<img src="/mb/images/javanio/nio-select-show.png">
`SelectNIOServerDemo` - 服务端
``` java
package org.mango.demo.selectnio;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.nio.charset.StandardCharsets;
import java.util.Iterator;
import java.util.Set;

/**
 * @Description 多路复用器版本 服务端
 * @Date 2021-10-03 13:40
 * @Created by mango
 */
public class SelectNIOServerDemo {
    public static void main(String[] args) throws IOException {
        ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
        int port = 9000;
        serverSocketChannel.bind(new InetSocketAddress(port));
        serverSocketChannel.configureBlocking(false);
        System.out.println("server listen on port " + port);

        // 设置多路复用器
        Selector selector = Selector.open();
        // 将serverSocketChannel的accept事件注册到多路复用器
        serverSocketChannel.register(selector, SelectionKey.OP_ACCEPT);
        while (true){
            // 查看selector.select()是否有事件准备就绪
            selector.select();
            Set<SelectionKey> selectionKeySet = selector.selectedKeys();
            Iterator<SelectionKey> iterable = selectionKeySet.iterator();
            while(iterable.hasNext()){
                SelectionKey selectionKey = iterable.next();
                // 将事件remove掉，防止重复处理
                iterable.remove();
                if(selectionKey.isAcceptable()){
                    // 得到连接的通道
                    SocketChannel socketChannel = serverSocketChannel.accept();
                    String socketName = socketChannel.toString();
                    System.out.println(socketName + " connect success!");
                    // 设置为非阻塞
                    socketChannel.configureBlocking(false);
                    // 注册读写事件到多路复用器
                    socketChannel.register(selector,SelectionKey.OP_READ);
                    // socketChannel.register(selector,SelectionKey.OP_WRITE);
                }else if(selectionKey.isReadable()){
                    // 得到可读的通道
                    SocketChannel socketChannel = (SocketChannel) selectionKey.channel();
                    String socketName = socketChannel.toString();
                    try {
                        // 读取数据并回写数据给客户端
                        ByteBuffer buffer = ByteBuffer.allocate(1024);
                        int len = socketChannel.read(buffer);
                        if (len == -1) {
                            System.out.println(socketName + " closed!");
                        }
                        if (len > 0) {
                            ByteBuffer data = ByteBuffer.allocate(len);
                            buffer.flip();
                            data.put(buffer);
                            String sData = new String(data.array(), StandardCharsets.UTF_8);
                            System.out.println(socketName + " receive data:" + sData);
                            // 回写数据
                            String tn = Thread.currentThread().getName();
                            String rData = sData + " - " + tn;
                            socketChannel.write(ByteBuffer.wrap(rData.getBytes(StandardCharsets.UTF_8)));
                        }
                    }catch (Exception e){
                        // 异常推出
                        socketChannel.close();
                        System.out.println(socketName + " exception close!");
                    }
                }
            }
        }
    }
}
```
执行结果：
``` java
/**
 * 执行结果：
 * server listen on port 9000
 * java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:57934] connect success!
 * java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:57934] receive data:123
 * java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:57934] receive data:你好
 * java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:57934] receive data:中国
 * java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:58056] connect success!
 * java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:58056] receive data:你呀
 * java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:58056] receive data:搞毛线哦
 * java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:58056] receive data:exit
 * java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:58056] exception close!
 * java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:57934] receive data:exit
 * java.nio.channels.SocketChannel[connected local=/127.0.0.1:9000 remote=/127.0.0.1:57934] exception close!
 */
```
`SelectNIOClientDemo` - 服务端
``` java
package org.mango.demo.selectnio;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.nio.charset.StandardCharsets;
import java.util.Iterator;
import java.util.Scanner;
import java.util.Set;

/**
 * @Date 2021-10-03 15:26
 * @Created by mango
 */
public class SelectNIOClientDemo {
    public static void main(String[] args) throws IOException, InterruptedException {
        SocketChannel sc = SocketChannel.open();
        String host = "127.0.0.1";
        int port = 9000;
        sc.connect(new InetSocketAddress(host,port));
        // 设置非阻塞
        sc.configureBlocking(false);
        System.out.println("connect server " + host + ":" + port + " success!");

        // 设置多路复用器，注册读事件
        Selector selector = Selector.open();
        sc.register(selector, SelectionKey.OP_READ);
        sc.register(selector, SelectionKey.OP_WRITE);
        // 从输入流中读取数据
        Scanner scanner = new Scanner(System.in);
        System.out.println("输入exit:客户端退出；其他为发送数据!");
        boolean loop = true;
        while (loop){
            // 查看多路复用器
            selector.select();
            Set<SelectionKey> selectionKeySet = selector.selectedKeys();
            Iterator<SelectionKey> iterator = selectionKeySet.iterator();
            while (iterator.hasNext()){
                SelectionKey selectionKey = iterator.next();
                // 移除掉事件，防止重复处理
                iterator.remove();
                if(selectionKey.isWritable()){
                    System.out.print("请输入:");
                    String input = scanner.next();
                    ByteBuffer data = ByteBuffer.wrap(input.getBytes(StandardCharsets.UTF_8));
                    // 发送数据
                    sc.write(data);
                    if("exit".equals(input)){
                        loop = false;
                    }
                }else if(selectionKey.isReadable()){
                    // 得到可读的通道
                    SocketChannel socketChannel = (SocketChannel) selectionKey.channel();
                    String socketName = socketChannel.toString();
                    // 读取数据并回写数据给客户端
                    ByteBuffer buffer = ByteBuffer.allocate(1024);
                    int len = socketChannel.read(buffer);
                    if(len == -1){
                        System.out.println(socketName + " closed!");
                    }
                    if(len > 0){
                        ByteBuffer data = ByteBuffer.allocate(len);
                        buffer.flip();
                        data.put(buffer);
                        String sData = new String(data.array(), StandardCharsets.UTF_8);
                        System.out.println(socketName + " receive data:" + sData);
                    }
                }
            }
        }
        // 关闭资源
        selector.close();
        sc.close();
        System.out.println("client exit");
    }
}
```
执行结果：
``` java
/**
 * 执行结果1：
 * connect server 127.0.0.1:9000 success!
 * 输入exit:客户端退出；其他为发送数据!
 * 请输入:你呀
 * 请输入:搞毛线哦
 * 请输入:exit
 * client exit
 */
```
``` java
/**
 * 执行结果2：
 * connect server 127.0.0.1:9000 success!
 * 输入exit:客户端退出；其他为发送数据!
 * 请输入:123
 * 请输入:你好
 * 请输入:中国
 * 请输入:exit
 * client exit
 */
```
***总结***
***1. 使用Selector选择器来实现多路复用器，调用select()方法得到就绪事件。***
***2.  socket关闭时，多路复用器会收到read事件，read到的字节-1。***