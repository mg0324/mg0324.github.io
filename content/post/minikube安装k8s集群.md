---
title: minikube安装k8s集群
date: 2021-11-21 22:10:55
categories: ["技术文章"]
tags: ["k8s","云原生","minikube"]
draft: false
---

[`minikube`](https://minikube.sigs.k8s.io/)是一个工具， 能让你在本地运行 Kubernetes。`minikube`在你本地的个人计算机（包括 Windows、macOS 和 Linux PC）运行一个单节点的 Kubernetes 集群，以便你来尝试 Kubernetes 或者开展每天的开发工作。


## 官方文档
https://minikube.sigs.k8s.io/docs/start/
## minikube安装k8s集群
1. 安装命令
``` bash
minikube start  
```
2. mac上安装示例
``` bash 
mango@mangodeMacBook-Pro ~ % minikube start  
  
😄  Darwin 10.15.7 上的 minikube v1.24.0  
✨  自动选择 hyperkit 驱动。其他选项：virtualbox, ssh  
💾  正在下载驱动 docker-machine-driver-hyperkit:  
❗  Unable to update hyperkit driver: download: getter: &{Ctx:context.Background Src:https://github.com/kubernetes/minikube/releases/download/v1.24.0/docker-machine-driver-hyperkit?checksum=file:https://github.com/kubernetes/minikube/releases/download/v1.24.0/docker-machine-driver-hyperkit.sha256 Dst:/Users/mango/.minikube/bin/docker-machine-driver-hyperkit.download Pwd: Mode:2 Umask:---------- Detectors:\[0x40ae630 0x40ae630 0x40ae630 0x40ae630 0x40ae630 0x40ae630 0x40ae630\] Decompressors:map\[bz2:0x40ae630 gz:0x40ae630 tar:0x40ae630 tar.bz2:0x40ae630 tar.gz:0x40ae630 tar.xz:0x40ae630 tar.zst:0x40ae630 tbz2:0x40ae630 tgz:0x40ae630 txz:0x40ae630 tzst:0x40ae630 xz:0x40ae630 zip:0x40ae630 zst:0x40ae630\] Getters:map\[file:0xc0008f2ba0 http:0xc000b5a180 https:0xc000b5a1a0\] Dir:false ProgressListener:0x406ffd0 Insecure:false Options:\[0x2448e00\]}: invalid checksum: Error downloading checksum file: Get "https://github.com/kubernetes/minikube/releases/download/v1.24.0/docker-machine-driver-hyperkit.sha256": dial tcp 20.205.243.166:443: i/o timeout  
💿  正在下载 VM boot image...  
    > minikube-v1.24.0.iso.sha256: 65 B / 65 B \[-------------\] 100.00% ? p/s 0s  
    > minikube-v1.24.0.iso: 225.58 MiB / 225.58 MiB \[ 100.00% 13.66 MiB p/s 17s  
👍  Starting control plane node minikube in cluster minikube  
💾  Downloading Kubernetes v1.22.3 preload ...  
    > preloaded-images-k8s-v13-v1...: 501.73 MiB / 501.73 MiB  100.00% 11.42 Mi  
🔥  Creating hyperkit VM (CPUs=2, Memory=2200MB, Disk=20000MB) ...  
🤦  StartHost failed, but will try again: new host: Driver "hyperkit" not found. Do you have the plugin binary "docker-machine-driver-hyperkit" accessible in your PATH?  
🔥  Creating hyperkit VM (CPUs=2, Memory=2200MB, Disk=20000MB) ...  
😿  Failed to start hyperkit VM. Running "minikube delete" may fix it: new host: Driver "hyperkit" not found. Do you have the plugin binary "docker-machine-driver-hyperkit" accessible in your PATH?  
❗  Startup with hyperkit driver failed, trying with alternate driver virtualbox: Failed to start host: new host: Driver "hyperkit" not found. Do you have the plugin binary "docker-machine-driver-hyperkit" accessible in your PATH?  
💀  Removed all traces of the "minikube" cluster.  
👍  Starting control plane node minikube in cluster minikube  
🔥  Creating virtualbox VM (CPUs=2, Memory=2200MB, Disk=20000MB) ...  
❗  This VM is having trouble accessing https://k8s.gcr.io  
💡  To pull new external images, you may need to configure a proxy: https://minikube.sigs.k8s.io/docs/reference/networking/proxy/  
🐳  正在 Docker 20.10.8 中准备 Kubernetes v1.22.3…  
    ▪ Generating certificates and keys ...  
    ▪ Booting up control plane ...  
    ▪ Configuring RBAC rules ...  
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5  
🌟  Enabled addons: storage-provisioner, default-storageclass  
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮  
│                                                                                                   │  
│    You have selected "virtualbox" driver, but there are better options !                          │  
│    For better performance and support consider using a different driver:                          │  
│            - hyperkit                                                                             │  
│                                                                                                   │  
│    To turn off this warning run:                                                                  │  
│                                                                                                   │  
│            $ minikube config set WantVirtualBoxDriverWarning false                                │  
│                                                                                                   │  
│                                                                                                   │  
│    To learn more about on minikube drivers checkout https://minikube.sigs.k8s.io/docs/drivers/    │  
│    To see benchmarks checkout https://minikube.sigs.k8s.io/docs/benchmarks/cpuusage/              │  
│                                                                                                   │  
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯  
🔎  Verifying Kubernetes components...  
  
❗  /usr/local/bin/kubectl is version 1.19.7, which may have incompatibilites with Kubernetes 1.22.3.  
    ▪ Want kubectl v1.22.3? Try 'minikube kubectl -- get pods -A'  
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```
3. 测试验证
``` bash
mango@mangodeMacBook-Pro ~ % kubectl get nodes
NAME  STATUS  ROLES AGE  VERSION
minikube  Ready control-plane,master  20h  v1.22.3
```
4. 开启dashboard
``` bash
mango@mangodeMacBook-Pro ~ % minikube dashboard
🤔 正在验证 dashboard 运行情况 ...
🚀 Launching proxy ...
🤔 正在验证 proxy 运行状况 ...
🎉 Opening http://127.0.0.1:61718/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/ in your default browser...
```

<img src="/mb/images/k8s/dashboard.png">
