## 服务器性能剖析

### MySQL status日志

```
#!/bin/sh

INTERVAL=5
PASSWORD='-uroot -p123abc.'
PREFIX=$INTERVAL-sec-status
RUNFILE=/home/fanghao/Desktop/MySQLRunning
mysql -e 'SHOW GLOBAL VARIABLES' $PASSWORD >> mysql-variables
while test -e $RUNFILE; do
   file=$(date +%F_%I)
   sleep=$(date +%s.%N | awk "{print $INTERVAL - (\$1 % $INTERVAL)}")
   sleep $sleep
   ts="$(date + "TS %s.%N %F %T")"
   loadavg="$(uptime)"
   echo "$ts $loadavg" >> $PREFIX-${file}-status
   mysql -e 'SHOW GLOBAL STATUS' $PASSWORD >> $PREFIX-${file}-status &
   echo "$ts $loadavg" >> $PREFIX-${file}-innodbstatus
   mysql -e 'SHOW ENGINE INNODB STATUS\G' >> $PREFIX-${file}-innodbstatus  &
   echo "$ts $loadavg" >> $PREFIX-${file}-processlist
   mysql -e 'SHOW FULL PROCESSLIST\G' $PASSWORD >> $PREFIX-${file}-processlist &
   echo $ts
done
echo Existing because $RUNFILE does not exist
```

### MySQL 单条查询效率查看

#### 使用SHOW PROFILING
```
SET PROFILING = 1;

SELECT * FROM sakila.nicer_but_slower_film_list;

SET @query_id = 1;

SELECT STATE, SUM(DURATION) AS TOTAL_R,
	ROUND(
		100 * SUM(DURATION) /
			(SELECT SUM(DURATION)
             FROM INFOMATION_SCHEMA.PROFILING
             WHERE QUERY_ID = @query_id
		), 2) AS PCT_R,
	COUNT(*) AS CALLS,
    SUM(DURATION) / COUNT(*) AS RCALL
FROM INFOMATION_SCHEMA.PROFILING
WHERE QUERY_ID = @query_id
GROUP BY STATE
ORDER BY TOTAL_R DESC;
```

#### 使用SHOW STATUS

```
FLUSH STATUS;
SELECT * FROM sakila.nicer_but_slower_film_list;
SHOW STATUS WHERE Variable_name like 'Handler%' or Variable_name like 'Create%';

Handler_read_rnd_next 值比较大的话可能没走索引
```

### 单条查询问题还是服务器问题

#### 使用mysqladmin
```
mysqladmin -hhost -P3306 -uroot -p ext -i1 | awk '/Queries/{q=$4-qp;qp=$4}/Threads_connected/{tc=$4}/Threads_running/{printf "%5d %5d %5d\n", q, tc, $4}'
Queries 每秒查询数
Threads_connected 如果使用了线程池则基本不太变化
Threads_running 正在执行查询线程数
如果服务器有问题，Queries会下降，其他两个则会有尖刺现象
```

### 其他mysqladmin查看mysql服务器状态

```
mysqladmin -P3306 -uroot -p -h127.0.0.1 -r -i 1 ext |\
awk -F"|" \
"BEGIN{ count=0; }"\
'{ if($2 ~ /Variable_name/ && ((++count)%20 == 1)){\
    print "----------|---------|--- MySQL Command Status --|----- Innodb row operation ----|-- Buffer Pool Read --";\
    print "---Time---|---QPS---|select insert update delete|  read inserted updated deleted|   logical    physical";\
}\
else if ($2 ~ /Queries/){queries=$3;}\
else if ($2 ~ /Com_select /){com_select=$3;}\
else if ($2 ~ /Com_insert /){com_insert=$3;}\
else if ($2 ~ /Com_update /){com_update=$3;}\
else if ($2 ~ /Com_delete /){com_delete=$3;}\
else if ($2 ~ /Innodb_rows_read/){innodb_rows_read=$3;}\
else if ($2 ~ /Innodb_rows_deleted/){innodb_rows_deleted=$3;}\
else if ($2 ~ /Innodb_rows_inserted/){innodb_rows_inserted=$3;}\
else if ($2 ~ /Innodb_rows_updated/){innodb_rows_updated=$3;}\
else if ($2 ~ /Innodb_buffer_pool_read_requests/){innodb_lor=$3;}\
else if ($2 ~ /Innodb_buffer_pool_reads/){innodb_phr=$3;}\
else if ($2 ~ /Uptime / && count >= 2){\
  printf(" %s |%9d",strftime("%H:%M:%S"),queries);\
  printf("|%6d %6d %6d %6d",com_select,com_insert,com_update,com_delete);\
  printf("|%6d %8d %7d %7d",innodb_rows_read,innodb_rows_inserted,innodb_rows_updated,innodb_rows_deleted);\
  printf("|%10d %11d\n",innodb_lor,innodb_phr);\
}}'
```

#### 通过SHOW PROCESSLIST显示线程状态

```
mysql -uroot -hhost -P3306 -p -e 'SHOW PROCESSLIST\G' |grep State: | sort | uniq -c | sort -rn
```


## Schema与数据类型优化

InnoDB 使用bit存储NULL，对于稀疏数据（多数值为NULL，少数的列非NULL）会有很好的空间效率，不适用MyISAM

DECIMAL比浮点类型消耗更大，对于及要求小数运算精确性，又要求性能的，可以选取BIGINT，相应的从小数变整数即可

存储UUID，应该移除'-'符号，或者最好使用UNHEX()转换为16字节数字，并存储在BINARY(16)列中，检索用HEX()格式化十六进制数字

太多的列、太多的关联（<12个最好）、枚举alter消耗大（选用整数型做外键关联到字典表比较合适）

引用技术表可以创建多行，防止update一行出现锁竞争，使用RAND() * count来随机选择一行，最后使用SUM()取总数


```
INSERT INTO tablename(values, values) VALUES(values, values) ON DUPLICATE KEY UPDATE values = values;
```

要关联的表字段一致，可以使用USING获得更好的性能

ALTER TABLE需要注意ALTER COLUMN，MODIFY COLUMN，CHANGE COLUMN的合适类型

## 创建高性能的索引

Memory引擎具有哈希索引（针对索引列的所有内容哈希，所以不支持范围查询）
InnoDB会有一个自适应哈希索引，会根据使用比较频繁的索引，在B-Tree索引之上在建立哈希索引，用户无法控制但可以关闭

自定义哈希索引


```
SELECT id FROM table_name WHERE filed="" AND filed_crc=CRC32("")
CREATE TABLE table_name (
 .................
 ................
 filed_crc IN UNSIGNED NOT NULL DEFAULT 0,
)
```
缺点是需要手工维护这个索引列
此书中使用的是创建触发器，但我觉得在项目里面可以写到代码里面执行insert
不使用SHA1()/MD5()的原因是慢、并且会生成很长的字符串
但CRC32在数据很大的时候可能会冲突
