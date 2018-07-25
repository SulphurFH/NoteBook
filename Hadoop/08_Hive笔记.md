在hive当中创建两张表

```
create table trade_detail (id bigint, account string, income double, expenses double, time string) row format delimited fields terminated by '\t';

create table user_info (id bigint, account string, name  string, age int) row format delimited fields terminated by '\t';
```
		
将mysq当中的数据直接导入到hive当中

```
sqoop import --connect jdbc:mysql://192.168.1.10:3306/itcast --username root --password 123 --table trade_detail --hive-import --hive-overwrite --hive-table trade_detail --fields-terminated-by '\t'
sqoop import --connect jdbc:mysql://192.168.1.10:3306/itcast --username root --password 123 --table user_info --hive-import --hive-overwrite --hive-table user_info --fields-terminated-by '\t'
```

创建一个result表保存前一个sql执行的结果

```
create table result row format delimited fields terminated by '\t' as select t2.account, t2.name, t1.income, t1.expenses, t1.surplus from user_info t2 join (select account, sum(income) as income, sum(expenses) as expenses, sum(income-expenses) as surplus from trade_detail group by account) t1 on (t1.account = t2.account);

create table user (id int, name string) row format delimited fields terminated by '\t'	
```
		
将本地文件系统上的数据导入到HIVE当中

```
load data local inpath '/root/user.txt' into table user;
```
		
创建外部表
```
create external table stubak (id int, name string) row format delimited fields terminated by '\t' location '/stubak';
```
		
创建分区表
普通表和分区表区别：有大量数据增加的需要建分区表

```
create table book (id bigint, name string) partitioned by (pubdate string) row format delimited fields terminated by '\t'; 
```

分区表加载数据

```
load data local inpath './book.txt' overwrite into table book partition (pubdate='2010-08-22');
```

练习

```
create table trade_detail(id bigint, account string, income double, expenses double, time string) row format delimited fields terminated by '\t';
create table user_info(id bigint, account string, name string, age int) row format delimited fields terminated by '\t'; 

load data local inpath '/home/hadoop/data/trade_detail' overwrite into table trade_detail;
load data local inpath '/home/hadoop/data/user_info' overwrite into table user_info;    

create table result row format delimited fields terminated by '\t' as select t1.account, t1.income, t1.expenses, t1.surplus, t2.name from user_info t2 join (select account, sum(income) as income, sum(expenses) as expenses, sum(income-expenses) as surplus from trade_detail group by account) t1 on(t1.account = t2.account);

创建外部表
create external table t_detail(id bigint, account string, income double, expenses double, time string) partitioned by (logdate string) row format delimited fields terminated by '\t' location '/hive/td_partition';

create temporary function AreaUDF as 'cn.itcast.hive.udf.AreaUDF';


load data inpath '/apache_cleaned/2013-05-31/part-r-00000'  into table hmbbs partition (logdate='2013-05-31');

pv

create table pv_2013_05_31 row format delimited fields terminated by '\t' as select count(*) from hmbbs where logdate='2013-05-31';

select count(distinct ip) from hmbbs where logdate='2013-05-31';

sqoop export --connect jdbc:mysql://192.168.8.103:3306/hmbbs --username root --password hadoop --export-dir '/user/hive/warehouse/pv_2013_05_31/000000_0' --table pv

SELECT COUNT(1) FROM (SELECT ip, COUNT(1) FROM hmbbs WHERE logdate='2013-05-31' GROUP BY ip HAVING COUNT(1)>50) t;
 
select t.ip, t.c from (SELECT ip, COUNT(1) as c FROM hmbbs WHERE logdate='2013-05-31' GROUP BY ip HAVING c>50) t order by t.c desc limit 10

SELECT COUNT(1) FROM hmbbs WHERE logdate='140421' AND instr(url, 'member.php?mod=register')>0;


create table result row format delimited fields terminated by '\t' as select t1.account, t1.name, t2.income, t2.expenses, t2.surplus from user_info t1 join (select account, sum(income) as income, sum(expenses) as expenses, sum(income-expenses) as surplus from trade_detail group by account) t2 on (t1.account = t2.account);

load data inpath '/out15/p*' into table hmbbs partition (logdate='2013-05-31');

select '2013-05-31', count (distinct ip) from hmbbs where logdate='2013-05-31';

SELECT COUNT(1) FROM hmbbs WHERE logdate='140314' AND instr(url, 'member.php?mod=register')>0;


select '140421', ip, count(ip) as cnum from hmbbs where logdate='140421' group by ip having cnum > 50 order by cnum desc limit 20;
```