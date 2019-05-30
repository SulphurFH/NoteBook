

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