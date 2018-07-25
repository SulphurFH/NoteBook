## 1.上传sqoop

## 2.安装和配置
解压

```
tar -zxvf sqoop-1.4.6.bin__hadoop-0.23.tar.gz -C /cloud
```

在添加sqoop到环境变量

```
export SQOOP_HOME=/cloud/sqoop-1.4.6
export PATH=$SQOOP_HOME/bin:$PATH
```

将数据库连接驱动(mysql-connector-java-5.1.45-bin.jar)拷贝到```$SQOOP_HOME/lib```里

## 3.使用

### 第一类：数据库中的数据导入到HDFS上

```
sqoop import --connect jdbc:mysql://hadoop03:3306/test --username root --password 123  --table trade_detail --columns 'id, account, income, expenses'
```
		
指定输出路径、指定数据分隔符

```
sqoop import --connect jdbc:mysql://hadoop03:3306/test --username root --password 123  --table trade_detail --target-dir '/sqoop/td' --fields-terminated-by '\t'
```
		
指定Map数量 -m

```
sqoop import --connect jdbc:mysql://hadoop03:3306/test --username root --password 123  --table trade_detail --target-dir '/sqoop/td1' --fields-terminated-by '\t' -m 2
```

增加where条件, 注意：条件必须用引号引起来

```
sqoop import --connect jdbc:mysql://hadoop03:3306/test --username root --password 123  --table trade_detail --where 'id>3' --target-dir '/sqoop/td2'
``` 

增加query语句(使用 \ 将语句换行)

```
sqoop import --connect jdbc:mysql://hadoop03:3306/test --username root --password 123 \
--query 'SELECT * FROM trade_detail where id > 2 AND $CONDITIONS' --split-by trade_detail.id --target-dir '/sqoop/td3'
```
		
⚠️ 如果使用--query这个命令的时候，需要注意的是where后面的参数，```AND $CONDITIONS``` 这个参数必须加上，而且存在单引号与双引号的区别，如果--query后面使用的是双引号，那么需要```$CONDITIONS```前加上```\```，即```\$CONDITIONS```，如果设置map数量为1个时即-m 1，不用加上```--split-by ${tablename.column}```，否则需要加上。
		
### 第二类：将HDFS上的数据导出到数据库中(不要忘记指定分隔符)

```
sqoop export --connect jdbc:mysql://hadoop03:3306/test --username root --password 123 --export-dir '/td3' --table td_bak -m 1 --fields-terminated-by ','
```
	

## 4.配置mysql远程连接

```
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123abc.' WITH GRANT OPTION;

FLUSH PRIVILEGES; 
```
	
⚠️ sqoop安装：安装在一台节点上就可以了。