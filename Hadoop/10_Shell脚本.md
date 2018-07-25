daily_clean.sh

```
#! /bin/bash

CURRENT=`date +%y%m%d`

/cloud/hadoop-2.6.5/bin/hadoop jar /root/Desktop/hadoop_jar/cleaner.jar /flume/$CURRENT /cleaned/$CURRENT

/cloud/hive-2.3.2/bin/hive -e "alter table hmbbs add partition (logdate=$CURRENT) location '/cleaned/$CURRENT';"

/cloud/hive-2.3.2/bin/hive -e "create table pv_$CURRENT row format delimited fields terminated by '\t' as select count(*) from hmbbs where logdate=$CURRENT;"

/cloud/hive-2.3.2/bin/hive -e "create table vip_$CURRENT row format delimited fields terminated by '\t' as select $CURRENT, ip, count(*) as hits from hmbbs where logdate=$CURRENT group by ip having hits > 20 order by hits desc limit 20;"

/cloud/sqoop-1.4.6/bin/sqoop export --connect jdbc:mysql://hadoop03:3306/hmbbs --username root --password 123abc. --export-dir "/user/hive/warehouse/vip_$CURRENT" --table VIP --fields-terminated-by '\t'
```