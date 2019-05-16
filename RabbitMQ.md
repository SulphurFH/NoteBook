# RabbitMQ

## 删除所有queue

```
rabbitmqctl set_policy deleter ".*" '{"expires":1}' --apply-to queues
```