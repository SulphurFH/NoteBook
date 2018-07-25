# 1. 准备集群环境
* 环境准备

```
CentOS-6.9-x86_64
jdk-8u151-linux-x64
zookeeper-3.4.10
```

此环境虚拟机准备3台，可以用之前虚拟机备份的，导入新建虚拟机

> 注意ip与hostsname分配

```
vim /etc/udev/rules.d/70-persistent-net.rules // 删除之前的eth0，将eth1改为eth0。

vim /etc/sysconfig/network-scripts/ifcfg-eth0 // 将步骤70-persistent-net.rules的HWADDR复制过来。

vim /etc/sysconfig/network  // 修改主机名

# reboot // 重启
```


# 2. 安装Zookeeper

```
tar -zxvf zookeeper-3.4.10.tar.gz -C /cloud
```

# 3. 修改Zookeeper配置文件

## 3.1 Zookeeper配置文件介绍

zookeeper的默认配置文件为zookeeper/conf/zoo_sample.cfg，需要将其修改为zoo.cfg。其中各配置项的含义，解释如下：

### 1.tickTime：CS通信心跳时间
Zookeeper 服务器之间或客户端与服务器之间维持心跳的时间间隔，也就是每个 tickTime 时间就会发送一个心跳。tickTime以毫秒为单位。
tickTime=2000  

### 2.initLimit：LF初始通信时限
集群中的follower服务器(F)与leader服务器(L)之间初始连接时能容忍的最多心跳数（tickTime的数量）。
initLimit=5  

### 3.syncLimit：LF同步通信时限
集群中的follower服务器与leader服务器之间请求和应答之间能容忍的最多心跳数（tickTime的数量）。
syncLimit=2  
 
### 4.dataDir：数据文件目录
Zookeeper保存数据的目录，默认情况下，Zookeeper将写数据的日志文件也保存在这个目录里。
dataDir=/home/michael/opt/zookeeper/data  

### 5.clientPort：客户端连接端口
客户端连接 Zookeeper 服务器的端口，Zookeeper 会监听这个端口，接受客户端的访问请求。
clientPort=2181 

### 6.服务器名称与地址：集群信息（服务器编号，服务器地址，LF通信端口，选举端口）
这个配置项的书写格式比较特殊，规则如下：
server.N=YYY:A:B 

```
server.1=hadoop01:2888:3888
server.2=hadoop02:2888:3888
server.3=hadoop03:2888:3888
```
> 我的配置如下：

```
# The number of milliseconds of each tick
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement
syncLimit=5
# the directory where the snapshot is stored.
# do not use /tmp for storage, /tmp here is just
# example sakes.
dataDir=/cloud/zookeeper-3.4.10/data
# the port at which the clients will connect
clientPort=2181
# the maximum number of client connections.
# increase this if you need to handle more clients
#maxClientCnxns=60
#
# Be sure to read the maintenance section of the
# administrator guide before turning on autopurge.
#
# http://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
#
# The number of snapshots to retain in dataDir
#autopurge.snapRetainCount=3
# Purge task interval in hours
# Set to "0" to disable auto purge feature
#autopurge.purgeInterval=1

server.1=hadoop01:2888:3888
server.2=hadoop02:2888:3888
server.3=hadoop03:2888:3888
```

## 3.2 Zookeeper临时文件创建

```
cd /cloud/zookeeper-3.4.10/
mdkir data
cd data
echo 1 >> myid		// hadoop01的主机保存为1，hadoop02保存为2，hadoop03保存为3，与server.1同步
```

# 4. 其他服务器的准备工作

## 4.1 配置文件复制

> 以下为hadoop01主机操作

```
cd ~/.ssh/
ssh-copy-id hadoop02
ssh-copy-id hadoop03
cd /cloud/zookeeper-3.4.10/conf
scp zoo.cfg root@hadoop02:/loud/zookeeper-3.4.10/conf
scp zoo.cfg root@hadoop03:/loud/zookeeper-3.4.10/conf
cd ..
scp -r data root@hadoop02:/loud/zookeeper-3.4.10
scp -r data root@hadoop03:/loud/zookeeper-3.4.10   // 注意修改相应主机的myid值
```


# 5. 测试

## 5.1 启动Zookeeper
> 3台主机依次运行启动

```
cd /cloud/zookeeper-3.4.10/bin
./zkServer.sh start
```

> 3台主机依次运行查看状态

```
./zkServer.sh status		// 如果有2个follower，1个leader表示成功
```

## 5.2 create查看是否数据同步

```
./zkCli.sh
create hadoopdata data
ls /hadoopdata
```
需其它两台主机也查看一下数据是否同步了

## 5.3 kill Leader Zookeeper是否成功故障转移

```
kill -9 leader Zookeeper sid
```
查看其它Zookeeper是否内部选举出新leader


