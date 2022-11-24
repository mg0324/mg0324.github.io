## 双部署

~~丢弃[https://mg0324.github.io/mb](https://mg0324.github.io/mb)~~

[http://mg.meiflower.top/mb](http://mg.meiflower.top/mb)

## 关于

博客基于hugo框架搭建

## 部署日志
``` shell
hugo server -b "http://hw.meiflower.top:30000/mb/" -p 30000 --bind "0.0.0.0"
# 整理上传
cp -r static/images/tool/ /data/mb/images
```
* 2022-11-24

  * 因为服务器过期，续费太贵，将k8s集群关闭，购买hw服务器1年
  * 将mg/mb博客迁移到hw服务器上，并使用docker-compose部署，挂载数据目录为/data/mb
* 2022-09-28

  * 从gitee pages迁移到k8s里的nginx-mb的helm charts
  * 图片资源放到node节点的/data/images和/data/img中
  * 其他资源放到node节点的/data/mb中

## 新建文章

```
hugo new 'post/java/java本地方法调用.md'
```
