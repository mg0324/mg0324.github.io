---
title: "SQL增强"
date: 2022-11-24T10:04:58+08:00
draft: false
categories: ["技术文章","数据库"]
tags: ["SQL"]
---

## Left Join

![](/mb/images/sql/left-join.drawio.svg)
左连接查询，以左边为主表。

```sql
select a.*,b.name from a left join b on a.id = b.a_id;
```

## Right Join

![](/mb/images/sql/right-join.drawio.svg)

右连接查询，以右边为主表。

```sql
select b.*,a.name from a right join b on a.id = b.a_id;
```

## Inner Join

![](/mb/images/sql/inner-join.drawio.svg)

内连接查询，以左右表交集。

```sql
select a.*,b.* from a inner join b on a.id = b.a_id;
```

## In

![](/mb/images/sql/in.drawio.svg)

范围查询

```sql
select a.* from a where a.id in ('1','3')
```

## Exist

![]( /mb/images/sql/exist.drawio.svg)

是否存在数据查询
``` sql
select * from a where exist (select 1 from b on a.id=b.a_id and b.grade>100)
```