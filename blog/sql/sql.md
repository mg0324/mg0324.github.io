## SQL增强

## Left Join

![](./left-join.drawio.svg)

左连接查询，以左边为主表。

```sql
select a.*,b.name from a left join b on a.id = b.a_id;
```

## Right Join

![](./right-join.drawio.svg)

右连接查询，以右边为主表。

```sql
select b.*,a.name from a right join b on a.id = b.a_id;
```

## Inner Join

![](./inner-join.drawio.svg)

内连接查询，以左右表交集。

```sql
select a.*,b.* from a inner join b on a.id = b.a_id;
```

## In

![](./in.drawio.svg)

范围查询

```sql
select a.* from a where a.id in ('1','3')
```

## Exist

![](./exist.drawio.svg)

是否存在数据查询
