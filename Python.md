# celery任务

## 本地开发启动
```
celery -A statis worker -l info
celery -A statis beat -l info
```

## 实时更新
```
sudo docker exec -it supervisor /bin/bash
source ../venv/bin/activate
```
## Ubuntu18.04 安装pip3问题
```
curl https://bootstrap.pypa.io/get-pip.py | sudo python3
```
