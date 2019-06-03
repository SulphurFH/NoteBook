

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
2. TCP
3. EXEC

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
```

## 服务发现

1. 环境变量
2. DNS
3. FQDN