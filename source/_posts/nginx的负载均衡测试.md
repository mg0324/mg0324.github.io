---
title: nginx的负载均衡测试
date: 2019-12-07 21:55:40
categories: nginx
tags:
- nginx
- test
- 负载均衡
---

# 疑问
在`nginx`中配置的最基本的`负载均衡`配置，是不是其中一个服务`挂掉`了，用户还是能够正常访问系统？

# 配置及环境
Nginx + node的http-server服务器 + 同一机器的2个端口web静态页服务
``` nginx
upstream web{
    #ip_hash;
    server 172.18.0.2:8001;
    server 172.18.0.2:8002;
}
```

``` nginx
location /web/ {
        proxy_pass http://web/;
}
```

# 测试
如下图gif所示

![](/mb/images/gif/nginx+http-server+upstream+test.gif)

# 结论
1. 2个服务都在跑的时候，能`负载均衡`到`web1`或者`web2`;
2. 当其中一个`挂掉`时，用户还是能`正常访问`，不会超时。

