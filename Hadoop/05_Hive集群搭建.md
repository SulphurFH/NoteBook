## 1.上传tar包
 
## 2.解压

```
tar -zxvf hive-0.9.0.tar.gz -C /cloud
```

## 3.配置mysql metastore（切换到root用户）

安装MySQL（hadoop03主机）

```
yum install mysql
```

修改密码，删除匿名用户

```
/usr/bin/mysql_secure_installation
（⚠️删除匿名用户，允许用户远程连接）
```

登陆mysql

```
mysql -u root -p

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123abc.' WITH GRANT OPTION;
FLUSH PRIVILEGES; 
```

## 4.配置hive

修改环境变量

```
vim /etc/profile

export HIVE_HOME=/cloud/hive-2.3.2
export PATH=$HIVE_HOME/bin:$PATH

source /etc/profile
```



修改hive-site.xml

```
cp hive-default.xml.template hive-site.xml
```

```
<configuration>
        <property>
                <name>javax.jdo.option.ConnectionURL</name>
                <value>jdbc:mysql://hadoop03:3306/metastore_db?createDatabaseIfNotExist=true</value>
                <description>JDBC connect string for a JDBC metastore</description>
        </property>

        <property>
                <name>javax.jdo.option.ConnectionDriverName</name>
                <value>com.mysql.jdbc.Driver</value>
                <description>Driver class name for a JDBC metastore</description>
        </property>

        <property>
                <name>javax.jdo.option.ConnectionUserName</name>
                <value>root</value>
                <description>username to use against metastore database</description>
        </property>

        <property>
                <name>javax.jdo.option.ConnectionPassword</name>
                <value>123abc.</value>
                <description>password to use against metastore database</description>
        </property>
</configuration>
```

MySQL初始化表

建库（hadoop03主机）

```
create database metastore_db charset=utf8;
```

拷贝脚本（hadoop01主机）

```
cd $HIVE_HOME/scripts/metastore/upgrade/mysql/
scp hive-schema-2.3.0.mysql.sql hadoop03:/root/Desktop
```

初始化表（hadoop03主机）

```
cd ~/Desktop
mysql -u root -p
source /root/Desktop/hive-schema-2.3.0.mysql.sql
```
	
## 5.拷贝MySQL连接驱动目录下

```
cp mysql-connector-java-5.1.45-bin.jar $HIVE_HOME/lib
```
	
	
⚠️Hive只在一个节点上安装即可