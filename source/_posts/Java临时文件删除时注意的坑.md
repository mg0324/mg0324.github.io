---
title: Java临时文件删除时注意的坑
date: 2021-01-05 18:56:13
categories: java
tags:
- java
- 文件删除
---

# 前言

最近在生产环境上发现了临时目录堆积吃掉大量磁盘的问题，最终原因是代码有Bug，异常后未执行`delete file`的代码或者执行了，但是删除失败。

# 解决思路

1. 将删除文件的代码放到`finally`块中。
2. 确保删除的文件未被使用。

# 例子

```java
String fdfsPath = null;
String dataHash = null;
String tmpPath = tmpDir + "/" + Tools.getUUID32() + ".json";
File tmpFile = new File(tmpPath);
try {
  FileUtil.writeUtf8String(hoJson.getJSONObject("data").toJSONString(), tmpFile);
  fdfsPath = fastDFSUtil.upload(tmpFile);
  dataHash = ManUtil.getSM3Str(FileUtil.readUtf8String(tmpFile)).toLowerCase();
}catch (Exception e){
  throw e;
}finally {
  //清理掉临时文件  确保能够执行，不然会导致临时文件堆积
  boolean b = FileUtil.del(tmpFile);
  logger.debug("删除临时文件" + tmpPath +" = " +b);
}
```

