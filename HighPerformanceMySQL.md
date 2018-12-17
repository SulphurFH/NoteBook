
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
