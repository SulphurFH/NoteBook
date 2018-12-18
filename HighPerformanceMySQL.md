
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
