# Docker
自己学习Docker记录的一些常用命令，平时查阅用

## Docker编译

```
# .表示使用当前路径下的Dockerfie文件
docker build -t fanghao/centos:7.1 .
```

## Docker镜像查看

```
docker images
```

## Docker启动镜像构建容器

```
#以交互式进入容器
docker run -it

#后台运行启动容器,返回一个container的id
docker run -d

#p与P的区别是一个指定宿主机端口映射，另一个随机分配宿主机端口映射，--name指定container的名字，后面跟要使用的容器名
docker run -d -p 2222:22 --name base fanghao/centos:7.1

# -e指定环境变量
docker run -d -p 80:80 --name wordpress -e WORDPRESS_DB_HOST=192.168.1.102 -e WORDPRESS_DB_USER=admin -e WORDPRESS_DB_PASSWORD=cspere2015 csphere/wordpress:4.2

 #创建一个容器，当他退出时就把他删除掉
docker run -it --rm csphere/cmd:0.1
```

## Docker容器查看

```
#查看本地所有状态的容器
docker ps -a

#查看本地正在运行的容器
docker ps
```

## Docker镜像删除

```
docker rmi

# 清理none镜像
docker rmi $(docker images | grep "none" | awk '{print $3}')

# 清理dangling镜像
docker rmi $(docker images -f "dangling=true" -q)
```

## Docker容器删除

```
# -f 为强制删除正在运行的容器
docker rm -f 'name'
docker rm

# 停止容器
docker stop $(docker ps -a | grep "Exited" | awk '{print $1 }')

# 删除容器
docker rm $(docker ps -a | grep "Exited" | awk '{print $1 }')
```

## Docker进入container

```
#以交互模式bash进入‘name’容器
docker exec -it 'name' /bin/bash
```

## Docker停止容器

```
docker stop 'name'
```

## Docker VOLUME

```
# VOLUME参数:之前的表示宿主机路径，之后表示容器内路径, 当container删除之后，VOLUME的数据会在还会一直保存在宿主机，重新创建一个container，指定之前的-v，可以恢复数据
docker run -d -p 3306:3306 -v /var/lib/docker/vfs/dir/mydata:/var/lib/mysql csphere/mysql:5.5
```

## Docker compose

```
# 使用docker-compose重启容器
sudo docker-compose -f etc/docker-compose-supervisor.yml down && sudo docker-compose -f etc/docker-compose-supervisor.yml up -d
```

## ENTRYPOINT和CMD

1. ENTRYPOINT定义容器启东市被调用的可执行程序
2. CMD指定传递给ENTRYPOINT的参数

这两条指令都支持shell和exec形式（区别在于命令是否在shell中被调用，shell进程往往是多余的，一般可以用exec）