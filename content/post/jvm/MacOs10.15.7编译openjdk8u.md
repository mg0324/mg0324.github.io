---
title: "MacOs10.15.7编译openjdk8u"
date: 2022-08-22T22:40:21+08:00
draft: false
categories: ["JVM"]
tags: ["java","jvm"]
---

## 机器环境及依赖
操作系统：`macOs 10.15.7`
BootJDK:   `/Library/Java/JavaVirtualMachines/jdk1.8.0_221.jdk/Contents/Home`
XCode：`Version 11.3.1 (11C505)`
hg命令(mercurial): `brew install mercurial`
freetype: `brew install freetype`
**注意：笔者先前打算编译jdk8，一番折腾后各种报错，最后选择jdk8u的版本。**
## 1.进入本机目录并下载源码
如果有代理请设置代理，不然可能会超时或者慢。
```
export http_proxys=http://127.0.0.1:9999
export http_proxy=http://127.0.0.1:9999
```
```
cd ~/git
mango@mangodeMacBook-Pro git % hg clone https://hg.openjdk.java.net/jdk8u/jdk8u/ openjdk8u
requesting all changes
adding changesets
adding manifests
adding file changes
added 2579 changesets with 3115 changes to 142 files
new changesets cfeea66a3fa8:a323800a7172
updating to branch default
86 files updated, 0 files merged, 0 files removed, 0 files unresolved
```
## 2.获取其他需要的存储库
```
您可以运行位于根存储库中的 get_source.sh 脚本来获取
  其他需要的存储库：
    cd openjdk8u && sh ./get_source.sh
```
该过程很慢，请耐心等待。
```
mango@mangodeMacBook-Pro openjdk8u % sh get_source.sh
# Repositories:  corba jaxp jaxws langtools jdk hotspot nashorn
                corba:   hg clone https://hg.openjdk.java.net/jdk8u/jdk8u/corba corba
                 jaxp:   hg clone https://hg.openjdk.java.net/jdk8u/jdk8u/jaxp jaxp
                 jaxp:   requesting all changes
                corba:   requesting all changes
                 jaxp:   adding changesets
                corba:   adding changesets
                corba:   adding manifests
                 jaxp:   adding manifests
                corba:   adding file changes
                 jaxp:   adding file changes
                corba:   added 2042 changesets with 4998 changes to 1392 files
                corba:   new changesets 55540e827aef:5cbb81265d86
                corba:   updating to branch default
                corba:   1198 files updated, 0 files merged, 0 files removed, 0 files unresolved
                jaxws:   hg clone https://hg.openjdk.java.net/jdk8u/jdk8u/jaxws jaxws
                jaxws:   requesting all changes
                jaxws:   adding changesets
                jaxws:   adding manifests
                jaxws:   adding file changes
                 jaxp:   added 2139 changesets with 8610 changes to 4242 files
                 jaxp:   new changesets 6ce5f4757bde:4356d7da8e0d
                 jaxp:   updating to branch default
                 jaxp:   2059 files updated, 0 files merged, 0 files removed, 0 files unresolved
            langtools:   hg clone https://hg.openjdk.java.net/jdk8u/jdk8u/langtools langtools
            langtools:   requesting all changes
            langtools:   adding changesets
            langtools:   adding manifests
            langtools:   adding file changes
                jaxws:   added 1933 changesets with 13926 changes to 6752 files
                jaxws:   new changesets 0961a4a21176:ec2d4135d03f
                jaxws:   updating to branch default
                jaxws:   3735 files updated, 0 files merged, 0 files removed, 0 files unresolved
                  jdk:   hg clone https://hg.openjdk.java.net/jdk8u/jdk8u/jdk jdk
                  jdk:   requesting all changes
                  jdk:   adding changesets
                  jdk:   adding manifests
            langtools:   added 3958 changesets with 22810 changes to 7200 files
            langtools:   new changesets 9a66ca7c79fa:bc8bc5deb3ae
            langtools:   updating to branch default
            langtools:   6402 files updated, 0 files merged, 0 files removed, 0 files unresolved
              hotspot:   hg clone https://hg.openjdk.java.net/jdk8u/jdk8u/hotspot hotspot
              hotspot:   requesting all changes
              hotspot:   adding changesets
              hotspot:   adding manifests
              hotspot:   adding file changes
              hotspot:   added 9532 changesets with 44715 changes to 6238 files
              hotspot:   new changesets a61af66fc99e:69087d08d473
              hotspot:   updating to branch default
              hotspot:   5266 files updated, 0 files merged, 0 files removed, 0 files unresolved
              nashorn:   hg clone https://hg.openjdk.java.net/jdk8u/jdk8u/nashorn nashorn
              nashorn:   requesting all changes
              nashorn:   adding changesets
              nashorn:   adding manifests
              nashorn:   adding file changes
                  jdk:   adding file changes
              nashorn:   added 2617 changesets with 11766 changes to 2994 files
              nashorn:   new changesets b8a1b238c77c:0761f5431f9d
              nashorn:   updating to branch default
              nashorn:   2775 files updated, 0 files merged, 0 files removed, 0 files unresolved
# Repositories:  jdk
                  jdk:   hg clone https://hg.openjdk.java.net/jdk8u/jdk8u/jdk jdk
                  jdk:   requesting all changes
                  jdk:   adding changesets
                  jdk:   adding manifests
                  jdk:   adding file changes
                  jdk:   added 14627 changesets with 107868 changes to 30915 files
                  jdk:   new changesets 37a05a11f281:7fcf35286d52
                  jdk:   updating to branch default
                  jdk:   25940 files updated, 0 files merged, 0 files removed, 0 files unresolved
# Repositories:  . corba jaxp jaxws langtools jdk hotspot nashorn
                    .:   cd . && hg pull -u
                corba:   cd corba && hg pull -u
                 jaxp:   cd jaxp && hg pull -u
                jaxws:   cd jaxws && hg pull -u
            langtools:   cd langtools && hg pull -u
                  jdk:   cd jdk && hg pull -u
              hotspot:   cd hotspot && hg pull -u
              nashorn:   cd nashorn && hg pull -u
                    .:   pulling from https://hg.openjdk.java.net/jdk8u/jdk8u/
                corba:   pulling from https://hg.openjdk.java.net/jdk8u/jdk8u/corba
                jaxws:   pulling from https://hg.openjdk.java.net/jdk8u/jdk8u/jaxws
                 jaxp:   pulling from https://hg.openjdk.java.net/jdk8u/jdk8u/jaxp
              hotspot:   pulling from https://hg.openjdk.java.net/jdk8u/jdk8u/hotspot
                  jdk:   pulling from https://hg.openjdk.java.net/jdk8u/jdk8u/jdk
              nashorn:   pulling from https://hg.openjdk.java.net/jdk8u/jdk8u/nashorn
            langtools:   pulling from https://hg.openjdk.java.net/jdk8u/jdk8u/langtools
                corba:   searching for changes
                corba:   no changes found
                  jdk:   searching for changes
                  jdk:   no changes found
                jaxws:   searching for changes
                jaxws:   no changes found
                 jaxp:   searching for changes
                 jaxp:   no changes found
              nashorn:   searching for changes
              nashorn:   no changes found
              hotspot:   searching for changes
              hotspot:   no changes found
                    .:   searching for changes
                    .:   no changes found
            langtools:   searching for changes
            langtools:   no changes found
```
## 3.检查配置bash ./configure
~~~
mango@mangodeMacBook-Pro openjdk8u % sh configure
Running generated-configure.sh
configure: Configuration created at Mon Aug 22 16:03:43 CST 2022.
configure: configure script generated at timestamp 1625670527.
checking for basename... /usr/bin/basename
checking for bash... /bin/bash
checking for cat... /bin/cat
checking for chmod... /bin/chmod
checking for cmp... /usr/bin/cmp
checking for comm... /usr/bin/comm
checking for cp... /bin/cp
checking for cut... /usr/bin/cut
checking for date... /bin/date
checking for gdiff... no
checking for diff... /usr/bin/diff
checking for dirname... /usr/bin/dirname
checking for echo... /bin/echo
checking for expr... /bin/expr
checking for file... /usr/bin/file
checking for find... /usr/bin/find
checking for head... /usr/bin/head
checking for ln... /bin/ln
checking for ls... /bin/ls
checking for mkdir... /bin/mkdir
checking for mktemp... /usr/bin/mktemp
checking for mv... /bin/mv
checking for nawk... no
checking for gawk... no
checking for awk... /usr/bin/awk
checking for printf... /usr/bin/printf
checking for rm... /bin/rm
checking for sh... /bin/sh
checking for sort... /usr/bin/sort
checking for tail... /usr/bin/tail
checking for tar... /usr/bin/tar
checking for tee... /usr/bin/tee
checking for touch... /usr/bin/touch
checking for tr... /usr/bin/tr
checking for uname... /usr/bin/uname
checking for uniq... /usr/bin/uniq
checking for wc... /usr/bin/wc
checking for which... /usr/bin/which
checking for xargs... /usr/bin/xargs
checking for gawk... no
checking for mawk... no
checking for nawk... no
checking for awk... awk
checking for grep that handles long lines and -e... /usr/bin/grep
checking for egrep... /usr/bin/grep -E
checking for fgrep... /usr/bin/grep -F
checking for a sed that does not truncate output... /usr/bin/sed
checking for cygpath... no
checking for greadlink... no
checking for readlink... /usr/bin/readlink
checking for df... /bin/df
checking for SetFile... /usr/bin/SetFile
checking for cpio... /usr/bin/cpio
checking build system type... x86_64-apple-darwin19.6.0
checking host system type... x86_64-apple-darwin19.6.0
checking target system type... x86_64-apple-darwin19.6.0
checking openjdk-build os-cpu... macosx-x86_64
checking openjdk-target os-cpu... macosx-x86_64
checking compilation type... native
checking for top-level directory... /Users/mango/git/openjdk8u
checking for presence of closed sources... no
checking if closed source is suppressed (openjdk-only)... no
checking which variant of the JDK to build... normal
checking which interpreter of the JVM to build... template
checking which variants of the JVM to build... server
checking which debug level to use... release
checking for sysroot...
checking for toolchain path...
checking for extra path...
checking where to store configuration... in default location
checking what configuration name to use... macosx-x86_64-normal-server-release
checking for apt-get... no
checking for yum... no
checking for port... no
checking for pkgutil... pkgutil
checking for gmake... no
checking for make... /usr/bin/make
configure: Testing potential make at /usr/bin/make, found using make in PATH
configure: Using GNU make 3.81 (or later) at /usr/bin/make (version: GNU Make 3.81)
checking if find supports -delete... yes
checking for unzip... /usr/bin/unzip
checking for zip... /usr/bin/zip
checking for ldd... no
checking for readelf... no
checking for greadelf... no
checking for hg... /Users/mango/envs/homebrew//bin/hg
checking for stat... /usr/bin/stat
checking for time... /usr/bin/time
checking for dsymutil... /usr/bin/dsymutil
checking for xattr... /usr/bin/xattr
checking for codesign... /usr/bin/codesign
checking if openjdk_codesign certificate is present... no
checking for pkg-config... /Users/mango/envs/homebrew//bin/pkg-config
checking pkg-config is at least version 0.9.0... yes
checking for 7z... no
checking for unzip... unzip
checking for wget... wget
checking headful support... include support for both headful and headless
checking whether to build JFR... true
configure: Found potential Boot JDK using JAVA_HOME
checking for Boot JDK... /Library/Java/JavaVirtualMachines/jdk1.8.0_221.jdk/Contents/Home
checking Boot JDK version... java version "1.8.0_221" Java(TM) SE Runtime Environment (build 1.8.0_221-b11) Java HotSpot(TM) 64-Bit Server VM (build 25.221-b11, mixed mode)
checking for java in Boot JDK... ok
checking for javac in Boot JDK... ok
checking for javah in Boot JDK... ok
checking for javap in Boot JDK... ok
checking for jar in Boot JDK... ok
checking for rmic in Boot JDK... ok
checking for native2ascii in Boot JDK... ok
checking if Boot JDK is 32 or 64 bits... 64
checking flags for boot jdk java command ...
checking flags for boot jdk java command for big workloads...  -Xms64M -Xmx1600M -XX:ThreadStackSize=1536
checking flags for boot jdk java command for small workloads...  -XX:+UseSerialGC -Xms32M -Xmx512M
configure: Xcode major version: 11
configure: Using default toolchain clang (clang/LLVM)
checking Determining if we need to set DEVELOPER_DIR... no
checking for xcodebuild... /usr/bin/xcodebuild
checking Determining Xcode SDK path... /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk
checking for clang... /usr/bin/clang
checking resolved symbolic links for CC... no symlink
configure: Using clang C compiler version 11.0.0 [Apple clang version 11.0.0 (clang-1100.0.33.17) Target: x86_64-apple-darwin19.6.0 Thread model: posix InstalledDir: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin]
checking whether the C compiler works... yes
checking for C compiler default output file name... a.out
checking for suffix of executables...
checking whether we are cross compiling... no
checking for suffix of object files... o
checking whether we are using the GNU C compiler... yes
checking whether /usr/bin/clang accepts -g... yes
checking for /usr/bin/clang option to accept ISO C89... none needed
checking for clang++... /usr/bin/clang++
checking resolved symbolic links for CXX... no symlink
configure: Using clang C++ compiler version 11.0.0 [Apple clang version 11.0.0 (clang-1100.0.33.17) Target: x86_64-apple-darwin19.6.0 Thread model: posix InstalledDir: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin]
checking whether we are using the GNU C++ compiler... yes
checking whether /usr/bin/clang++ accepts -g... yes
checking how to run the C preprocessor... /usr/bin/clang -E
checking how to run the C++ preprocessor... /usr/bin/clang++ -E
checking for ar... ar
configure: Rewriting AR to "/usr/bin/ar"
checking for gcc... gcc
checking whether we are using the GNU Objective C compiler... yes
checking whether gcc accepts -g... yes
configure: Rewriting OBJC to "/usr/bin/gcc"
checking for lipo... /usr/bin/lipo
checking for strip... strip
configure: Rewriting STRIP to "/usr/bin/strip"
checking for otool... /usr/bin/otool
checking for nm... nm
configure: Rewriting NM to "/usr/bin/nm"
checking for gobjdump... no
checking for objdump... objdump
configure: Rewriting OBJDUMP to "/usr/bin/objdump"
checking for jtreg... no
checking for ANSI C header files... yes
checking for sys/types.h... yes
checking for sys/stat.h... yes
checking for stdlib.h... yes
checking for string.h... yes
checking for memory.h... yes
checking for strings.h... yes
checking for inttypes.h... yes
checking for stdint.h... yes
checking for unistd.h... yes
checking stdio.h usability... yes
checking stdio.h presence... yes
checking for stdio.h... yes
checking size of int *... 8
checking for target address size... 64 bits
checking whether byte ordering is bigendian... no
checking if the C compiler supports "-m64"... yes
checking if the C++ compiler supports "-m64"... yes
checking if both compilers support "-m64"... yes
checking if the C compiler supports "-m64"... yes
checking if the C++ compiler supports "-m64"... yes
checking if both compilers support "-m64"... yes
checking if we should generate debug symbols... true
checking if we should zip debug-info files... yes
checking what type of native debug symbols to use (this will override previous settings)... not specified
configure: --with-native-debug-symbols not specified. Using values from --disable-debug-symbols and --disable-zip-debug-info
checking what is not needed on MacOSX?... alsa pulse x11
checking for X... no
checking for X11/extensions/shape.h... no
checking cups/cups.h usability... yes
checking cups/cups.h presence... yes
checking for cups/cups.h... yes
checking cups/ppd.h usability... yes
checking cups/ppd.h presence... yes
checking for cups/ppd.h... yes
checking for FREETYPE... yes
checking for freetype... yes (using pkg-config)
checking if we can compile and link with freetype... yes
checking if we should bundle freetype... no
checking for main in -ljpeg... no
configure: Will use jpeg decoder bundled with the OpenJDK source
checking for which giflib to use... bundled
checking for compress in -lz... yes
checking for which zlib to use... system
checking for cos in -lm... yes
checking for dlopen in -ldl... yes
checking if elliptic curve crypto implementation is present... yes
checking for number of cores... 2
checking for memory size... 8192 MB
checking for appropriate number of jobs to run in parallel... 2
checking whether to use sjavac... no
checking is ccache enabled... no
checking if build directory is on local disk... yes
configure: creating /Users/mango/git/openjdk8u/build/macosx-x86_64-normal-server-release/config.status
config.status: creating /Users/mango/git/openjdk8u/build/macosx-x86_64-normal-server-release/spec.gmk
config.status: creating /Users/mango/git/openjdk8u/build/macosx-x86_64-normal-server-release/hotspot-spec.gmk
config.status: creating /Users/mango/git/openjdk8u/build/macosx-x86_64-normal-server-release/bootcycle-spec.gmk
config.status: creating /Users/mango/git/openjdk8u/build/macosx-x86_64-normal-server-release/compare.sh
config.status: creating /Users/mango/git/openjdk8u/build/macosx-x86_64-normal-server-release/spec.sh
config.status: creating /Users/mango/git/openjdk8u/build/macosx-x86_64-normal-server-release/Makefile
config.status: creating /Users/mango/git/openjdk8u/build/macosx-x86_64-normal-server-release/config.h
config.status: /Users/mango/git/openjdk8u/build/macosx-x86_64-normal-server-release/config.h is unchanged
found it

====================================================
A new configuration has been successfully created in
/Users/mango/git/openjdk8u/build/macosx-x86_64-normal-server-release
using default settings.

Configuration summary:
* Debug level:    release
* JDK variant:    normal
* JVM variants:   server
* OpenJDK target: OS: macosx, CPU architecture: x86, address length: 64

Tools summary:
* Boot JDK:       java version "1.8.0_221" Java(TM) SE Runtime Environment (build 1.8.0_221-b11) Java HotSpot(TM) 64-Bit Server VM (build 25.221-b11, mixed mode)  (at /Library/Java/JavaVirtualMachines/jdk1.8.0_221.jdk/Contents/Home)
* Toolchain:      clang (clang/LLVM)
* C Compiler:     Version 11.0.0 (at /usr/bin/clang)
* C++ Compiler:   Version 11.0.0 (at /usr/bin/clang++)

Build performance summary:
* Cores to use:   2
* Memory limit:   8192 MB

WARNING: The result of this configuration has overridden an older
configuration. You *should* run 'make clean' to make sure you get a
proper build. Failure to do so might result in strange build problems.
~~~

## 4.检查配置通过后，编译make
执行make images命令，编译过程耗时比较久，请耐心等待。
```
$ make images
省略大部分日志......
----- Build times -------
Start 2022-08-22 16:20:35
End   2022-08-22 16:44:13
00:00:26 corba
00:10:12 demos
00:04:55 hotspot
00:02:17 images
00:00:15 jaxp
00:00:26 jaxws
00:04:15 jdk
00:00:34 langtools
00:00:18 nashorn
00:23:38 TOTAL
-------------------------
Finished building OpenJDK for target 'images'
```
看到如上输出后，说明编译镜像成功。会在build下有images的目录，如下图：
![](/mb/images/jvm2/jdk8u/01.png)
## 5.测试
进入到目录（因机器而已）：/Users/mango/git/openjdk8u/build/macosx-x86_64-normal-server-release/images/j2sdk-image/bin，后执行`java -version`。可以将`j2sdk-bundle`下的软件包copy到`/Library/Java/JavaVirtualMachines`下，在IDEA中配置使用。
```
mango@mangodeMacBook-Pro bin % ./java -version
openjdk version "1.8.0-internal"
OpenJDK Runtime Environment (build 1.8.0-internal-mango_2022_08_22_16_19-b00)
OpenJDK 64-Bit Server VM (build 25.71-b00, mixed mode)
```

## 参考文档
在编译过程中，可能会遇到各种各样的问题，这里就不标出来了。（因为不太懂C，要怎么解决也都是查资料尝试解决的。）
> 参考地址：https://github.com/openjdk/jdk/tree/jdk8-b120
> 参考博客：https://blog.csdn.net/lizhengjava/article/details/105629780/
