# celery任务

> 本地开发启动
```
celery -A statis worker -l info
celery -A statis beat -l info
```

> 统计系统，实时更新
```
sudo docker exec -it ak_saas_statis_supervisor /bin/bash
source ../venv/bin/activate
```
