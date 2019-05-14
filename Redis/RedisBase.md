## Redis一些常用命令总结

Redis DEL

```
# DEL命令不支持通配符，但是可以结合Linux管道和xargs命令实现
redis-cli KEYS "user:*" | xargs redis-cli DEL
```