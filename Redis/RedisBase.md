# Redis 自己少用/不知道的命令总结

Redis对于键的命名没有强制要求，但是比较好的实践是用“对象类型:对象ID:对象属性”

例如：user:1:friends，对于多个单词推荐用“.”分隔

Redis DEL

```
# DEL命令不支持通配符，但是可以结合Linux管道和xargs命令实现
redis-cli KEYS "user:*" | xargs redis-cli DEL
```

## 字符串

```
# 递增数字（原子操作，保证事务一致性），做累加操作会是个好的应用场景
INCR key
INCRBY key increment
DECR key
DECRBY key decrement
INCRBYFLOAT key increment
```

## Hash

HSET不区分插入和更新操作（插入返回1，更新返回0）
HGETALL 返回字段和字段值的列表
HSETNX与HSET命令类似，如果字段存在，HSETNX将不执行任何操作

```
HINCRBY key field increment
```