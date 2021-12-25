---
title: 基于helm将芒果卡片部署到k8s
categories: k8s
tags:
  - k8s
  - kubernetes
abbrlink: 87ba7257
date: 2021-08-27 14:54:10
---

## 缘起

在工作中，因为一名姓万的项目管理者，对我们提出了个人项目小卡片的征集活动。我写了3个任务，读一本技术书籍，开发卡片项目V1.0版本，和考驾照。

<!--more-->

到目前为止，基本已经完成。

* 读了有好几本技术数据，包括《spring Cloud与Docker微服务架构实战》、《重学Java设计模式》、《Redis设计与实现》等。

* 卡片项目命名为**芒果卡片**，已经迭代到v3.1版本。

* 驾照已经在2019年拿到。

学习了docker后，完成了芒果卡片部署的容器化；学习了k8s后，今天也算是完成了芒果卡片的k8s化。

## 发展历程

* 2018年开发第一版，部署在裸机云服务器ESC上

* 2019年开发第二版，部署在docker容器内，数据库由mysql切换为内存数据库sqlite

* 2020年开发第三版，实现卡片扫码录入，随机卡片，答题模式等。

* 2021年继续迭代，集成芒果网盘，点子队列，更新日志，卡片统计和卡片上传图片到阿里云oss中等功能。

  今天，通过这篇文章，记录一下芒果卡片的k8s化部署。

## 部署架构图

<img src="/mb/images/k8s-card.png">

## 实际操作

### 构建helm3的Charts

<img src="/mb/images/k8s-card-helm-dir.png">

#### configmap.yaml  基于configmap管理springboot程序的配置文件

**特别注意，key后面的 | 竖线，不给竖线的话，application.properties里的内容在挂着到容器内部后不会换行，导致配置文件错误。**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: card-config
  namespace: {{.Values.namespace}}
data:
  application.properties: |
     server.port=9001
     server.servlet.context-path=/card
     #日志相关配置
     logging.config=classpath:logback-dev.xml
     #spring json返回数据格式化
     spring.jackson.date-format=yyyy-MM-dd HH:mm:ss
     #spring json 时区
     spring.jackson.time-zone=GMT+8


     #================================================数据源配置==============================================================
     #数据源驱动类
     spring.datasource.driverClassName=org.sqlite.JDBC
     #数据源链接地址
     spring.datasource.url=jdbc:sqlite:/data/sqlite/card2.db
     #数据源账号
     spring.datasource.username=
     #数据源密码
     spring.datasource.password=
     spring.datasource.druid.db-type=sqlite
     #数据源连接池初始化连接数
     spring.datasource.initialSize=5
     #数据源连接池最小空闲连接数
     spring.datasource.minIdle=5
     #数据源连接池最大连接数
     spring.datasource.maxActive=10
     #数据源连接池最大等待时间，单位毫秒
     spring.datasource.maxWait=60000
     #数据源过滤器
     spring.datasource.filters=stat,wall,slf4j
     #开启druid监控
     spring.datasource.connectionProperties=druid.stat.mergeSql=true;druid.stat.slowSqlMillis=5000
     #================================================数据源配置==============================================================

     #================================================mybatis配置=============================================================
     #mybatis xml配置文件
     mybatisp-plus.config-locations=classpath*:mybatis/mybatis-config.xml
     #mybatis mapper xml所在位置加装
     mybatis-plus.mapper-locations=classpath*:mybatis/mappers/**/*.xml
     # 设置mybatis返回值为空是也返回key
     mybatis-plus.configuration.call-setters-on-nulls=true
     #查询结果自动映射 到 java类中驼峰命名
     mybatis-plus.configuration.map-underscore-to-camel-case=true
     #================================================mybatis配置=============================================================

     #================================================redis配置=============================================================
     spring.redis.host=x.x.x.x
     spring.redis.port=1111
     spring.redis.password=xx@
     # 连接池最大连接数(使用负值表示没有限制) 默认为8
     spring.redis.lettuce.pool.max-active=8
     # 连接池最大阻塞等待时间(使用负值表示没有限制) 默认为-1
     spring.redis.lettuce.pool.max-wait=-1ms
     # 连接池中的最大空闲连接 默认为8
     spring.redis.lettuce.pool.max-idle=8
     # 连接池中的最小空闲连接 默认为 0
     spring.redis.lettuce.pool.min-idle=0
     #================================================redis配置=============================================================

     card.job.hot.cron=0 0/5 * * * ?
```

#### cron-job.yaml - 基于cronjob + python完成sqlite数据库定时备份

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: card-cronjob
  namespace: {{.Values.namespace}}
spec:
  schedule: {{.Values.app.emailBackCron}}
  jobTemplate:
    spec:
      backoffLimit: 3
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: card-cronjob
            image: python:3.6.14-alpine
            command: ["python3", "email_back.py"]
            workingDir: /opt
            volumeMounts:
            - name: sqlite-v
              mountPath: /opt
          volumes:
          - name: sqlite-v
            hostPath:
              path: /nfsdata
```

#### deployment.yaml 基于deployment完成pod的部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{.Values.app.name}}
  namespace: {{.Values.namespace}}
  labels:
    app: {{.Values.app.name}}
spec:
  replicas: {{.Values.app.replicas}}
  selector:
    matchLabels:
      app: {{.Values.app.name}}
  template:
    metadata:
      labels:
        app: {{.Values.app.name}}
    spec:
      containers:
      - name: {{.Values.app.name}}
        image: {{.Values.app.image}}
        imagePullPolicy: IfNotPresent
        env:
        - name: APP_CONFIG
          value: {{.Values.app.env.config}}
        - name: JAVA_OPTS
          value: {{.Values.app.env.javaOpts}}
        ports:
        - containerPort: {{.Values.app.targetPort}}
        volumeMounts:
        - name: card-cm
          mountPath: /opt/config
        - name: sqlite-v
          mountPath: /data/sqlite
        resources:
          requests:
            memory: "100Mi"
            cpu: "200m"
          limits:
            memory: "300Mi"
            cpu: "500m"
      volumes:
      - name: card-cm
        configMap:
          name: card-config
          items:
          - key: application.properties
            path: application.properties
      - name: sqlite-v
        persistentVolumeClaim:
          claimName: card-pvc
```

#### pv.yaml

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: card-pv
  namespace: {{.Values.namespace}}
  labels:
    type: card-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Recycle
  hostPath:
    path: /nfsdata

```

#### pvc.yaml

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: card-pvc
  namespace: {{.Values.namespace}}
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  selector:
    matchLabels:
      type: card-pv
```

#### service.yaml - 基于svc的nodePort暴露服务

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{.Values.app.name}}
  namespace: {{.Values.namespace}}
  labels:
    name: {{.Values.app.name}}
spec:
  type: NodePort
  ports:
    - port: {{.Values.app.targetPort}}
      targetPort: {{.Values.app.targetPort}}
      protocol: TCP
      nodePort: {{.Values.app.nodePort}}
  selector:
    app: {{.Values.app.name}}
```

#### values.yaml

基于helm的value封装对模板文件内的值，达到集中配置集中修改的效果。

```yaml
# 命名空间
namespace: default
# 应用相关
app:
  # 应用名称
  name: card-api
  # 应用副本数
  replicas: 1
  # 应用镜像
  image: mangomei/card:k8s-v5-3.1
  env:
    # 应用配置
    config: /opt/config/application.properties
    # jvm 参数
    javaOpts:
  # 容器端口
  targetPort: 9001
  # svc端口
  nodePort: 32091
  # 每天中午12点备份，容器内时间 +8 小时
  emailBackCron: "0 4 * * *"
```



### 基于helm3完成部署

* 初次安装，`helm install card-api .`
* 更新release，`helm upgrade card-api .`

```bash
[root@master card-api]# helm upgrade card-api .
Release "card-api" has been upgraded. Happy Helming!
NAME: card-api
LAST DEPLOYED: Fri Aug 27 14:11:53 2021
NAMESPACE: default
STATUS: deployed
REVISION: 20
TEST SUITE: None
```

## 效果展示

<img src="/mb/images/k8s-dashboard.png">

<img src="/mb/images/k8s-card-1.png" width="300px">

<img src="/mb/images/k8s-card-2.jpeg" width="300px">

<img src="/mb/images/k8s-card-3.png" width="300px">

<img src="/mb/images/k8s-card-4.png" width="300px">

## 总结

1. 学海无涯，永无止境。学了就要用，用的合理不合理先别太关心。
2. 开始了的项目一定要继续坚持，半途而废可耻。
3. 从物理机，虚拟机，云服务器，docker，k8s，跟上时代步伐一路前行。
4. helm是k8s的包管理工具，能开始部署一个项目内需要的各个k8s组件，构建集群。