

## Minikube安装

```
# 采用阿里镜像，国内用官方太慢
curl -Lo minikube http://kubernetes.oss-cn-hangzhou.aliyuncs.com/minikube/releases/v1.1.0/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
```

```
minikube start --registry-mirror=https://registry.docker-cn.com
```

## 创建Pod

```
创建pod
kubectl run kubia --image=luksa/kubia --port=8080 --generator=run-pod/v1
kubectl get nodes
kubectl get svc
# 告知k8s创建ReplicationController
kubectl expose rc kubia --type=LoadBalancer --name kubia-http
# minikube不支持LoadBalancer，所以不会有EXTERNAL-IP
minikube server kubia-http
```

## 水平伸缩

```
kubectl scale rc kubia --replicas=3
```

## 基于yaml创建pod

```
kubectl create -f ***.yaml
```

## 向Pod发送请求

1. kubectl expose创建service
2. kubectl port-forward kubia-manual 8888:8080

## 新增Lables

```
kubectl label pod kubia-manual creation_method=manual
kubectl label pod kubia-manual-v2 env=debug --overwrite
```

## 命名空间

```
kubectl create namespace custom-namespace
```

## 删除pod

```
kubectl delete pod pod-name1 pod-name2
kubectl delete pod -l xxxx=xxxx
```

ReplicationController控制的pod，删除了会自己重建，所以要先删除rc


## 查看k8s资源信息

```
kubectl explain
```

## Liveness Probe

1. http探针
2. TCP探针
3. EXEC探针

## 查看log

```
# 查看当前
kubectl logs pod
# 查看前一个（pod重启）
kubectl logs pod --previous
```

## 查看描述

```
kubectl describe pod pod-name
# 其中ExitCode表示退出码，137表示进程被外部信号终止，128+9（SIGKILL）， 143对应128+15（SIGTERM）
```

## 删除rc

```
# 设置--cascade=false不会删除rc管理的pod
kubectl delete rc rc-name --cascade=false
```

RC会在之后的版本移除，改为ReplicationSets

## DaemonSet

负责运行系统服务（让节点上都有要运行的pod，如日志，资源监控）

## Job

## CronJob

## Services

```
# 创建服务
kubectl expose
# 或者通过yaml创建
kubectl create -f svc.yaml
```

```
# -- 代表这kubectl命令的结束，后面的将是在pod内部执行的命令
kubectl exec pod-name -- curl -s http://service:ip
kubectl exec -it pod-name bash
kubectl exec -it pod-name -c container-name -- /bin/bash
```

## 服务发现

1. 环境变量
2. DNS
3. FQDN

## 连接集群外部服务

endpoints

endpoint对象需要与服务具有相同的名称，这样服务就可以具有像pod选择器那样的服务正常使用

## 服务暴露给外部客户端

1. NodePort
2. LoadBalance
3. Ingress

```
# 使用JSONPath获取所有节点IP
kubectl get nodes -o jsonpath='{.item[*].status.addresses[?(@.type=="ExternalIP")].address}'
```

svc的spec -> externalTrafficPolicy:Local 可以防止不必要的网络跳数，但是可能会导致跨pod的负载分布不均匀

## Ingress

Ingress一般指向一个NodePort

```
# Ingress TLS
kubectl create secret tls tls-secret --cert=tls.cert --key=tls.key
kubectl edit ingress ingress-name

tls:
- hosts:
    - hostname
    secretName: tls-name
```

## Readiness Probe

1. http探针
2. TCP探针
3. EXEC探针

应该通过删除pod或者更改pod标签而不是手动更改探针来从服务中手动移除pod

1. 务必定义就绪探针
2. 不要将停止pod的逻辑纳入就绪探针中


## Headless

提供跨pod负载均衡，但是是通过DNS轮询机制不是通过服务代理

## 卷
 
 hostPath是持久性存储，新pod还可以发现上个pod保留的数据，但是要求必须和上一个pod在统一节点


 ```
 # 获得pod运行在哪个节点
 kubectl get po -o wide
 ```

 持久卷和持久卷生命只能被统一命名空间的pod创建使用

 StorageClass

 动态配置的持久卷其容量和访问模式是在PVC中所要求的


 ## 覆盖命令和参数

|   Docker   | k8s |
| ---------- | --- |
| ENTRYPOINT | command |
| CMD | args |


可以为Pod的容器中设置环境变量（从Pod层面设定环境变量同样有效，目前尚不支持）

硬编码环境变量可能对生产测试的Pod要严格区分定义，可以使用ConfigMap解耦


```
kubectl create configmap configmap-name --from-literal=key1=value1 --from-literal=key2=value2
kubectl create configmap configmap-name --from-file=config-file.conf # 也可以将整个文件夹导入
```

configMap条目作为环境变量传递给pod（ValueForm）

Pod引用ConfigMap中不存在的键会造成容器启动失败，创建了所需的configMap后，失败的容器会自动启动

将卷挂载至某一个文件夹，意味着容器镜像中文件夹下原本存在的任何文件都会被隐藏，可以使用subPath

修改configMap后，可以支持手动通知容器更新

```
# 更新nginx文件
kubectl edit configmap configmap-name
kubectl exec pod-name -c container-name -- nginx -s reload
```

Secret只会储存在节点的内存中（存储的为Base64编码，不止用来存储文本还可以存储二进制）

secret最好不要通过环境变量暴露给容器