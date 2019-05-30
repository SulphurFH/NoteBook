

# Minikube安装

```
# 采用阿里镜像，国内用官方太慢
curl -Lo minikube http://kubernetes.oss-cn-hangzhou.aliyuncs.com/minikube/releases/v1.1.0/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
```

```
minikube start --registry-mirror=https://registry.docker-cn.com
```