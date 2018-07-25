# 1. 集群搭建规划：

### 个人感觉比较好的资源分配
	
主机名 | IP | 安装的软件 | 运行的进程
----|------|----------|------|
hadoop01 | 192.168.1.140 | jdk、hadoop| NameNode、DFSZKFailoverController |
hadoop02 | 192.168.1.141  | jdk、hadoop| NameNode、DFSZKFailoverController |
hadoop03 | 192.168.1.142 | jdk、hadoop| ResourceManager |
hadoop04 | 192.168.1.143 | jdk、hadoop、zookeeper| DataNode、NodeManager、JournalNode、QuorumPeerMain |
hadoop05 | 192.168.1.144 | jdk、hadoop、zookeeper| DataNode、NodeManager、JournalNode、QuorumPeerMain |
hadoop06 | 192.168.1.145 | jdk、hadoop、zookeeper| DataNode、NodeManager、JournalNode、QuorumPeerMain |

> 说明：
	在hadoop2.0中通常由两个NameNode组成，一个处于active状态，另一个处于standby状态。Active NameNode对外提供服务，而Standby NameNode则不对外提供服务，仅同步active namenode的状态，以便能够在它失败时快速进行切换。
	hadoop2.0官方提供了两种HDFS HA的解决方案，一种是NFS，另一种是QJM。这里我们使用简单的QJM。在该方案中，主备NameNode之间通过一组JournalNode同步元数据信息，一条数据只要成功写入多数JournalNode即认为写入成功。通常配置奇数个JournalNode
	这里还配置了一个zookeeper集群，用于ZKFC（DFSZKFailoverController）故障转移，当Active NameNode挂掉了，会自动切换Standby NameNode为standby状态

### 资源不足，目前只用了这种，这种不好因为NameNode和ResourceManager都需要不少资源，最好分开。但是下面的配置文件配置是按照6台机子写的

主机名 | IP | 安装的软件 | 运行的进程
----|------|----------|------|
hadoop01 | 192.168.1.140 | jdk、hadoop、zookeeper| NameNode、DFSZKFailoverController、QuorumPeerMain |
hadoop02 | 192.168.1.141 | jdk、hadoop、zookeeper| NameNode、DFSZKFailoverControlle、ResourceManager、QuorumPeerMain |
hadoop03 | 192.168.1.142 | jdk、hadoop、zookeeper| DataNode、NodeManager、JournalNode、QuorumPeerMain |

	
# 2. 安装步骤
## 2.1 安装配置zooekeeper集群

> 详见02_Zookeeper集群搭建
	
## 2.2 安装配置hadoop集群

### 2.2.1 解压

```
tar -zxvf hadoop-2.6.5.tar.gz -C /cloud/
```

### 2.2.2 配置HDFS
> hadoop2.0所有的配置文件都在$HADOOP_HOME/etc/hadoop目录下

```
#将hadoop添加到环境变量中
vim /etc/profile

export JAVA_HOME=/usr/java/jdk1.8.0_151
export JRE_HOME=/usr/java/jdk1.8.0_151/jre
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib
export HADOOP_HOME=/cloud/hadoop-2.6.5
export PATH=$JAVA_HOME/bin:$HADOOP_HOME/bin:$PATH
```
			
### 2.2.3 修改hadoo-env.sh

```
export JAVA_HOME=/usr/java/jdk1.8.0_151
```
				
### 2.2.4 修改core-site.xml

```
<configuration>
	<!-- 指定hdfs的nameservice为ns1 -->
	<property>
		<name>fs.defaultFS</name>
		<value>hdfs://ns1</value>
	</property>
	<!-- 指定hadoop临时目录 -->
	<property>
		<name>hadoop.tmp.dir</name>
		<value>/cloud/hadoop-2.6.5/tmp</value>
	</property>
	<!-- 指定zookeeper地址 -->
	<property>
		<name>ha.zookeeper.quorum</name>
		<value>hadoop01:2181,hadoop02:2181,hadoop03:2181</value>
	</property>
</configuration>
```
				
### 2.2.5 修改hdfs-site.xml

```				
<configuration>
	<!--指定hdfs的nameservice为ns1，需要和core-site.xml中的保持一致 -->
	<property>
		<name>dfs.nameservices</name>
		<value>ns1</value>
	</property>
	<!-- ns1下面有两个NameNode，分别是nn1，nn2 -->
	<property>
		<name>dfs.ha.namenodes.ns1</name>
		<value>nn1,nn2</value>
	</property>
	<!-- nn1的RPC通信地址 -->
	<property>
		<name>dfs.namenode.rpc-address.ns1.nn1</name>
		<value>hadoop01:9000</value>
	</property>
	<!-- nn1的http通信地址 -->
	<property>
		<name>dfs.namenode.http-address.ns1.nn1</name>
		<value>hadoop01:50070</value>
	</property>
	<!-- nn2的RPC通信地址 -->
	<property>
		<name>dfs.namenode.rpc-address.ns1.nn2</name>
		<value>hadoop02:9000</value>
	</property>
	<!-- nn2的http通信地址 -->
	<property>
		<name>dfs.namenode.http-address.ns1.nn2</name>
		<value>hadoop02:50070</value>
	</property>
	<!-- 指定NameNode的元数据在JournalNode上的存放位置 -->
	<property>
		<name>dfs.namenode.shared.edits.dir</name>
		<value>qjournal://hadoop04:8485;hadoop05:8485;hadoop06:8485/ns1</value>
	</property>
	<!-- 指定JournalNode在本地磁盘存放数据的位置 -->
	<property>
		<name>dfs.journalnode.edits.dir</name>
		<value>/cloud/hadoop-2.6.5/journal</value>
	</property>
	<!-- 开启NameNode失败自动切换 -->
	<property>
		<name>dfs.ha.automatic-failover.enabled</name>
		<value>true</value>
	</property>
	<!-- 配置失败自动切换实现方式 -->
	<property>
		<name>dfs.client.failover.proxy.provider.ns1</name>
		<value>org.apache.hadoop.hdfs.server.namenode.ha.ConfiguredFailoverProxyProvider</value>
	</property>
	<!-- 配置隔离机制方法，多个机制用换行分割，即每个机制暂用一行-->
	<property>
		<name>dfs.ha.fencing.methods</name>
		<value>
			sshfence
			shell(/bin/true)
		</value>
	</property>
	<!-- 使用sshfence隔离机制时需要ssh免登陆 -->
	<property>
		<name>dfs.ha.fencing.ssh.private-key-files</name>
		<value>/root/.ssh/id_rsa</value>
	</property>
	<!-- 配置sshfence隔离机制超时时间 -->
	<property>
		<name>dfs.ha.fencing.ssh.connect-timeout</name>
		<value>30000</value>
	</property>
</configuration>
```
			
### 2.2.6 修改mapred-site.xml

```
<configuration>
	<!-- 指定mr框架为yarn方式 -->
	<property>
		<name>mapreduce.framework.name</name>
		<value>yarn</value>
	</property>
</configuration>	
```
			
### 2.2.7 修改yarn-site.xml

```
<configuration>
	<!-- 指定resourcemanager地址 -->
	<property>
		<name>yarn.resourcemanager.hostname</name>
		<value>hadoop03</value>
	</property>
	<!-- 指定nodemanager启动时加载server的方式为shuffle server -->
	<property>
		<name>yarn.nodemanager.aux-services</name>
		<value>mapreduce_shuffle</value>
	</property>
</configuration>
```
			
				
### 2.2.8 修改slaves
> slaves是指定子节点的位置，因为要在hadoop01上启动HDFS、在hadoop03启动yarn，所以hadoop01上的slaves文件指定的是datanode的位置，hadoop03上的slaves文件指定的是nodemanager的位置

```
hadoop04
hadoop05
hadoop06
```

### 2.2.9 配置免密码登陆
> 首先要配置hadoop01到hadoop02、hadoop03、hadoop04、hadoop05、hadoop06的免密码登陆

在hadoop01上生产一对钥匙

```
ssh-keygen -t rsa
```

将公钥拷贝到其他节点，包括自己

```
ssh-coyp-id hadoop01
ssh-coyp-id hadoop02
ssh-coyp-id hadoop03
ssh-coyp-id hadoop04
ssh-coyp-id hadoop05
ssh-coyp-id hadoop06
```
				
配置hadoop03到hadoop04、hadoop05、hadoop06的免密码登陆
在hadoop03上生产一对钥匙

```
ssh-keygen -t rsa
```

将公钥拷贝到其他节点

```
ssh-coyp-id hadoop04
ssh-coyp-id hadoop05
ssh-coyp-id hadoop06
```

注意：两个namenode之间要配置ssh免密码登陆，别忘了配置hadoop02到hadoop01的免登陆

在hadoop02上生产一对钥匙

```
ssh-keygen -t rsa
ssh-coyp-id -i hadoop01		
```
		
		
## 2.3 将配置好的hadoop拷贝到其他节点

```
scp -r hadoop-2.6.5/ root@hadoop02:/cloud
scp -r hadoop-2.6.5/ root@hadoop03:/cloud
scp -r hadoop-2.6.5/ root@hadoop04:/cloud
scp -r hadoop-2.6.5/ root@hadoop05:/cloud
scp -r hadoop-2.6.5/ root@hadoop06:/cloud
```

⚠️ 以下顺序严格执行
## 2.4 启动zookeeper集群
> 分别在hadoop04、hadoop05、hadoop06上启动zk

```
cd /cloud/zookeeper-3.4.10/bin/
./zkServer.sh start
#查看状态：一个leader，两个follower
./zkServer.sh status
```
			
## 2.5 启动journalnode
> 在hadoop01上启动所有journalnode，注意：是调用的hadoop-daemons.sh这个脚本，注意是复数s的那个脚本

```
cd /cloud/hadoop-2.6.5
sbin/hadoop-daemons.sh start journalnode
#运行jps命令检验，hadoop04、hadoop05、hadoop06上多了JournalNode进程
```
		
## 2.6 格式化HDFS
> ⚠️在hadoop01上执行命令:

```
hdfs namenode -format
```

格式化后会在根据core-site.xml中的hadoop.tmp.dir配置生成个文件，这里我配置的是/itcast/hadoop-2.2.0/tmp，然后将/itcast/hadoop-2.2.0/tmp拷贝到itcast02的/itcast/hadoop-2.2.0/下。

```
scp -r tmp/ root@hadoop02:/cloud/hadoop-2.6.5/
```
	
## 2.7 格式化ZK
> 在hadoop01上执行即可

```			
hdfs zkfc -formatZK
```	
运行zkCli后查看／目录即可看到[zookeeper, hadoop-ha]
## 2.8 启动HDFS
> 在hadoop01上执行

```
sbin/start-dfs.sh
```

## 2.9 启动YARN
⚠️是在hadoop03上执行start-yarn.sh，把namenode和resourcemanager分开是因为性能问题，因为他们都要占用大量资源，所以把他们分开了，他们分开了就要分别在不同的机器上启动

```
sbin/start-yarn.sh
```
到此，hadoop2.6.5配置完毕，可以统计浏览器访问:

```
http://hadoop01:50070
NameNode 'hadoop01:9000' (active)
http://hadoop01:50070
NameNode 'hadoop02:9000' (standby)
```

# 3. NameNode发生故障启动
```
cd $HADOOP_HOME
sbin/hadoop-daemon.sh start namenode
```