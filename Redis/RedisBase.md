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

## 列表

列表向两端添加元素的时间复杂度为O(1)，对于从两端取某些数据速度非常快，但是访问索引只能循环遍历

LLEN的复杂度为O(1)，Redis会直接读取现成的值

LRANGE返回值包含最右边的元素


```
# 删除列表中前count个值为value的元素
LREM key count value
count > 0 从左边删除前count个值为value
count < 0 从右边删除前count个值为value
count = 0 删除所有值为value
```

使用LTRIM和LPUSH来限制列表中元素的数量

```
# 保留最近100条日志
LPUSH logs $newLog
LTRIM logs 0 99
```

多个队列传递数据可以使用RPOPLPUSH


## 集合

插入、删除、判断存在复杂度都是O(1)


```
SADD key member
SREM key
SMEMBERS key
SISMEMBER key
```