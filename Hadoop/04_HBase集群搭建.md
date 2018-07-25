# 1.上传hbase安装包

# 2.解压

```
tar -zxvf hbase-1.3.1-bin.tar.gz -C /cloud
```


# 3.配置hbase集群

* 首先要安装好Zookeeper集群

* 要把hadoop的hdfs-site.xml和core-site.xml 放到hbase/conf下

### 3.1 修改hbase-env.sh
```
export JAVA_HOME=/usr/java/jdk1.7.0_55
//告诉hbase使用外部的zk 
export HBASE_MANAGES_ZK=false
```

### 3.2 修改hbase-site.xml

```
vim /cloud/hbase-1.3.1/conf/hbase-site.xml
<configuration>
	<property>
                <name>hbase.rootdir</name>
                <value>hdfs://ns1/hbase</value>
        </property>
		<!-- 指定hbase是分布式的 -->
        <property>
                <name>hbase.cluster.distributed</name>
                <value>true</value>
        </property>
		<!-- 指定zk的地址，多个用“,”分割 -->
        <property>
                <name>hbase.zookeeper.quorum</name>
                <value>hadoop01:2181,hadoop02:2181,hadoop03:2181</value>
        </property>
</configuration>
```
### 3.3 修改regionservers

```
vim /cloud/hbase-1.3.1/conf/regionservers
hadoop03
hadoop04
hadoop05
hadoop06
```
	
### 3.3拷贝hbase到其他节点

```
scp -r /cloud/hbase-1.3.1 hadoop02:/cloud/
scp -r /cloud/hbase-1.3.1 hadoop03:/cloud/
scp -r /cloud/hbase-1.3.1 hadoop04:/cloud/
scp -r /cloud/hbase-1.3.1 hadoop05:/cloud/
scp -r /cloud/hbase-1.3.1 hadoop06:/cloud/
```

# 4.将配置好的HBase拷贝到每一个节点并同步时间。

# 5.启动所有的hbase
> 分别启动zk

```
./zkServer.sh start
```
> 启动hadoop集群

```
./start-dfs.sh
```

> 启动hbase，在主节点上运行

```
./start-hbase.sh
```

# 6.通过浏览器访问hbase管理页面
http://hadoop01:16010/
# 7.为保证集群的可靠性，要启动多个HMaster
```
./hbase-daemon.sh start master
```