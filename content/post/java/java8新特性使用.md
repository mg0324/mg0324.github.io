---
title: java8新特性使用
date: 2022-11-24 11:38:20
categories: ["技术文章","Java"]
tags: ["jdk8","新特性"]
draft: false
---

## Stream api

### Collect to Map

```java
Map<String, String> result = effectList.stream().collect(
            Collectors.toMap(BusiDisposalProveEffectInfo::getDeclareId,
                            BusiDisposalProveEffectInfo::getRegAttachmentId));
```

### Collect to List or Set

```java
List<String> idList = resultList.stream().map(BusiDisposalProveListVO::getId).collect(Collectors.toList());
```

### Filter

```java
Set<String> idSet = resultList.stream()
                .filter(e -> StringUtils.equals(e.getStatus(), DeclareStatusEnum.SUCCESS.getCode()))
                .map(BusiDisposalProveListVO::getId)
                .collect(Collectors.toSet());
```

## Consumer

```java
// 相加并将结果回调回去
public void f1(int a,int b,Consumer<Integer> callback){
  callback.accept(a+b);
}
// 调用并打印
f1(1,2,result -> {
  System.out.println(result);
})
```
