---
title: k8s的相关发行版
categories: 运维
tags:
  - k8s
  - 云原生
abbrlink: a4e5670
date: 2021-11-21 22:24:23
---

2021-11-20 周6
## 因子
自2015年google开源kubernetes后，到目前为止市面上出现了很多发行版。大部分是国外的，也有国内的，下面探讨下一些最近接触到的。（全世界900多个linux发行版，30多个k8s发行版）

|  发行版   |  时间   |  组织   |  网址 |
| --- | --- | --- | --- |
|  k8s   |  2014.11.15   |  google   | https://kubernetes.io/ |
|  openshift   |  2015.05   |  Red Hat   | https://www.redhat.com/zh/technologies/cloud-computing/openshift |
|  k3s   |  2019   |   Rancher Labs | https://www.rancher.cn/k3s/ |
|  rancher   |  2019   |   Rancher Labs | https://www.rancher.cn/ |
|  k0s   |  2020.12    |  Mirantis   | https://k0sproject.io/ |
|  MicroK8s   |  2020   |  Canonical  | https://microk8s.io/ |
|  kubesphere   |  2019.04   |   QingClound（青云 * 国内）  | https://kubesphere.io/zh/ |
|  kubeoperator   |  2020   |  FitClound(飞致云 * 国内）   |  https://kubeoperator.io/ |

## 理解及体会
虽然k8s发行版很多，但是内核基本上和k8s差不多，都是将服务器资源集群化，利用yaml或者json配置，创建不同资源，以容器运行，对外暴露服务的过程。像轻量级的k3s，k0s，microK8s，都是结合自身应用场景，将安装部署简单化，无用组件删减化的产物。


