# 1. 准备Linux环境
* 环境准备

```
CentOS-6.9-x86_64
jdk-8u151-linux-x64
hadoop-2.6.5
```
	
## 1.1 修改主机名

```shell
vim /etc/sysconfig/network
NETWORKING=yes
HOSTNAME=hadoop01
```
 
## 1.2 修改IP

```shell
vim /etc/sysconfig/network-scripts/ifcfg-eth0
			
DEVICE="eth0"
BOOTPROTO="static"
HWADDR="00:0C:29:3C:BF:E7"
IPV6INIT="yes"
NM_CONTROLLED="yes"
ONBOOT="yes"
TYPE="Ethernet"
UUID="ce22eeca-ecde-4536-8cc2-ef0dc36d4a8c"
IPADDR="192.168.1.140"
NETMASK="255.255.255.0"
GATEWAY="192.168.1.1"
```
HWADDR 通过
```
ifconfig
```
查看eth0来获取
UUID 通过
```
uuidgen eth0
```
来获取

			
## 1.3 修改主机名和IP的映射关系

```shell
vim /etc/hosts
192.168.1.140	hadoop01
```
	
## 1.4 关闭防火墙
* 查看防火墙状态 
```service iptables status```

* 关闭防火墙
```service iptables stop```

* 查看防火墙开机启动状态
```chkconfig iptables --list```

* 关闭防火墙开机启动
```chkconfig iptables off```
	

## 1.5 重启Linux

```
reboot
```

# 2. 安装JDK
	
## 2.1 解压jdk

* 创建文件夹
```		
mkdir /usr/java
```

* 解压
```
tar -zxvf jdk-8u151-linux-x64.tar.gz -C /usr/java/
```
		
## 2.2 将java添加到环境变量中
* 修改配置文件

```
vim /etc/profile
export JAVA_HOME=/usr/java/jdk1.8.0_151
export JRE_HOME=/usr/java/jdk1.8.0_151/jre
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib
export PATH=$JAVA_HOME/bin:$PATH
```

* 刷新配置

```
source /etc/profile
```
		
# 3. 安装hadoop2.6.5

## 3.1 解压hadoop

```
mkdir /cloud
tar -zxvf hadoop-2.6.5.tar.gz -C /cloud
```

## 3.2 配置hadoop
* 进入hadoop配置目录

```
cd /cloud/hadoop-2.6.5/etc/hadoop
```

* hadoop-env.sh

```
vim hadoop-env.sh

修改export JAVA_HOME=${JAVA_HOME}为
export JAVA_HOME=/usr/java/jdk1.8.0_151
```
		
* core-site.xml

```
<!-- 制定HDFS的master（NameNode）的地址 -->
<property>
	<name>fs.defaultFS</name>
	<value>hdfs://hadoop01:9000</value>
</property>
<!-- 指定hadoop运行时产生文件的存储目录 -->
<property>
	<name>hadoop.tmp.dir</name>
	<value>/cloud/hadoop-2.6.5/tmp</value>
</property>
```
		
* hdfs-site.xml

```
<!-- 指定HDFS副本的数量，伪分布式为1 -->
<property>
	<name>dfs.replication</name>
	<value>1</value>
</property>
```
		
* mapred-site.xml (cp mapred-site.xml.template mapred-site.xml)

```
<!-- 指定mr运行在yarn上 -->
<property>
	<name>mapreduce.framework.name</name>
	<value>yarn</value>
</property>
```
		
* yarn-site.xml

```
<!-- 指定YARN的master（ResourceManager）的地址 -->
<property>
	<name>yarn.resourcemanager.hostname</name>
	<value>hadoop01</value>
</property>
<!-- reducer获取数据的方式 -->
<property>
	<name>yarn.nodemanager.aux-services</name>
	<value>mapreduce_shuffle</value>
</property>
```
	
## 3.3 将hadoop添加到环境变量

```
vim /etc/proflie
export JAVA_HOME=/usr/java/jdk1.8.0_151
export JRE_HOME=/usr/java/jdk1.8.0_151/jre
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib
export HADOOP_HOME=/cloud/hadoop-2.6.5
(直接复制上面的覆盖之前java的即可)

source /etc/profile
```
	
## 3.4 格式化namenode（对namenode进行初始化）

```
hdfs namenode -format (hadoop namenode -format)
		
日志中出现表示成功格式化：
17/11/19 21:28:38 INFO common.Storage: Storage directory /cloud/hadoop-2.6.5/tmp/dfs/name has been successfully formatted.
```
		
## 3.5 启动hadoop

```
cd /cloud/hadoop-2.6.5/
```

* 先启动HDFS

```
sbin/start-dfs.sh
```
		
* 再启动YARN

```
sbin/start-yarn.sh
```
		
## 3.6 验证是否启动成功

* 使用jps命令验证

```
jps

4754 ResourceManager
4341 NameNode
4456 DataNode
5146 Jps
5035 NodeManager
4607 SecondaryNameNode
```
	
> http://192.168.1.140:50070 （HDFS管理界面）
> 
> http://192.168.1.140:8088 （MR管理界面）

## 3.7 测试HDFS上传与下载


```
hadoop fs -put XXX.file hdfs://hadoop01:9000/jdk
hadoop fs -get hdfs://hadoop01:9000/jdk ./
```

## 3.8 测试YARN与MapReduce

```
cd $HADOOP_HOME/share/hadoop/mapreduce

[root@hadoop01 mapreduce]# vim work
hello tom
hello jerry
hello world
hello kitty
hello tom
保存做测试

[root@hadoop01 mapreduce]# hadoop fs -put work hdfs://hadoop01:9000/words

[root@hadoop01 mapreduce]# hadoop fs -ls hdfs://hadoop01:9000/
Found 2 items
-rw-r--r--   1 root supergroup  189736377 2017-11-19 14:34 hdfs://hadoop01:9000/jdk
-rw-r--r--   1 root supergroup         56 2017-11-19 15:44 hdfs://hadoop01:9000/words

[root@hadoop01 mapreduce]# hadoop jar hadoop-mapreduce-examples-2.6.5.jar wordcount hdfs://hadoop01:9000/words hdfs://hadoop01:9000/wcout

[root@hadoop01 mapreduce]# hadoop fs -get hdfs://hadoop01:9000/wcout ./

[root@hadoop01 mapreduce]# cd wcout/

[root@hadoop01 wcout]# ls
part-r-00000  _SUCCESS
[root@hadoop01 wcout]# cat part-r-00000
hello	5
jerry	1
kitty	1
tom	2
world	1
```

# 4. SSH免登录
* 生成ssh免登陆密钥

```
cd ~／.ssh／
ssh-keygen -t rsa （四个回车）
```

* 将公钥拷贝到要免登陆的机器上

```
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
或
ssh-copy-id -i localhost
```

* 其他服务器发送公钥

```
ssh-copy-id hadoop02
```

# 5. FAQ

## 5.1 WARN问题

* 运行上传与下载时会发现出现如下警告⚠️

```
WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
```

> 执行hdfs dfs -ls / 查看原因为libhadoop.so需要的glibc版本是glibc_2.14
> 
> 查看当前系统的glibc版本，如下：

```
[root@hadoop01 native]$ ldd --version

ldd (GNU libc) 2.12

Copyright (C) 2010 Free Software Foundation, Inc.

```

**解决方法1**

配置```$HADOOP_HOME/etc/hadoop/log4j.properties/log4j.properties```文件来忽略掉这个警告

```
log4j.logger.org.apache.hadoop.util.NativeCodeLoader=ERROR
```


**解决方法2**

升级系统的glib版本

下载glibc-2.14.tar.bz2，地址为：http://ftp.ntu.edu.tw/gnu/glibc/

下载glibc-linuxthreads-2.5.tar.bz2，地址为：http://ftp.ntu.edu.tw/gnu/glibc/

> 安装步骤如下：

更新gcc 

```
sudo yum install gcc-c++
```

把下载的bz2包放到一个文件夹下

```
[root@hadoop01 glib]# ls

glibc-2.14.tar.bz2 glibc-linuxthreads-2.5.tar.bz2
```

解压glibc-2.14.tar.bz2到当前目录

```
[root@hadoop01 glib]# tar -xjvf glibc-2.14.tar.bz2

[root@hadoop01 glib]# ls

glibc-2.14.tar.bz2 glibc-2.14 glibc-linuxthreads-2.5.tar.bz2
```

解压glibc-linuxthreads-2.5.tar.bz2到glibc-2.14中

```
[root@hadoop01 glib]# cd glibc-2.14

[root@hadoop01 glibc-2.14]# tar -xjvf ../glibc-linuxthreads-2.5.tar.bz2
```

此时，glibc-2.14目录下会多出两个文件夹，即linuxthreads和linuxthreads_db

回到上一级目录，执行如下命令：

```
[root@hadoop01 glibc-2.14]# cd ..
//加上优化开关，否则会出现错误'#error "glibc cannot be compiled without optimization"'
[root@hadoop01 glib]# export CFLAGS="-g -O2"
[root@hadoop01 glib]# glibc-2.14/configure --prefix=/usr --disable-profile --enable-add-ons --with-headers=/usr/include --with-binutils=/usr/bin --disable-sanity-checks
```

执行make

```
//编译，执行很久(5-10分钟)，可能出错，出错再重新执行

[root@hadoop01 glib]# make
```

执行make install

```
[root@hadoop01 glib]# make install

```

使用命令ls -l /lib/libc.so.6查看是否升级成功

```
[root@hadoop01 glib]# ll /lib64/libc.so.6
lrwxrwxrwx. 1 root root 12 Nov 19 23:05 /lib64/libc.so.6 -> libc-2.14.so
```

重启hadoop

```
cd $HADOOP_HOME
cd sbin
./start-dfs.sh
./start-yarn.sh
```

执行一条hdfs命令，发现本地库被成功加载

```
[root@hadoop01 ~]$ export HADOOP_ROOT_LOGGER=DEBUG,console

[root@hadoop01 ~]$ hdfs dfs -ls /
```