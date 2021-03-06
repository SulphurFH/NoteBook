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
SDIFF
SINTER
SUNION
SCARD # 集合元素数量
SPOP # 集合是无序的所以无法LPOP或者RPOP
```

```
# 0 < count < SMEMBERS key 返回count个元素
# count >= SMEMBERS key 返回key的所有元素
# count < 0 返回|count|个key的元素，可能有重复
SRANDMEMBER key [count]
```

## 有序集合

```
ZADD key score member
ZSCORE key member
ZRANGE key start stop [WITHSCORES]
ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]
ZREVRANGEBYSCORE的min和max参数是相反的
```

## 事务

```
# 如果命令语法错误，那么EXEC会返回错误，连语法正确的命令也不执行（开发时就要规避）
# 运行错误会继续执行
MULI
COMMANDS
EXEC
```

WATCH命令监控一个或多个键，一旦被修改（删除），事务就不会被执行

## 过期键

PERSIST命令将键恢复成永久（成功清除过期时间返回1， 键不存在或键本来就是永久的返回0）

场景1

10分钟 100次

伪代码

```
list_len = LLEN rate.limiting:id
if list_len < 10:
    LPUSH rate.limiting:id now()
else:
    time = LINDEX rate.limiting:id -1
    if now() - time < 60:
        print 超过限制
    else:
        LPUSH rate.limiting:id now()
        LTRIM rate.limiting:id 0, 9
```

## 排序

SORT支持对集合、列表、有序集合类型进行排序


```
SORT [BY pattern] key [LIMIT] [ASC|DESC] [ALPHA] [STORE]
```

```
127.0.0.1:6379> LPUSH sortbylist 1 2 3 4 5
(integer) 5
127.0.0.1:6379> SET itemscore:1 100
OK
127.0.0.1:6379> SET itemscore:2 70
OK
127.0.0.1:6379> SET itemscore:3 270
OK
127.0.0.1:6379> SET itemscore:4 20
127.0.0.1:6379> SORT sortbylist BY itemscore:* DESC
1) "3"
2) "1"
3) "2"
4) "4"
5) "5"
```

"*"只能在"->"符号前面，后面的会被当做字段名本身

STORE结合EXPIRE缓存排序结果

```
is_exist = EXISTS cache_sort
if is_exist:
    return LRANGE cache_sort 0, -1
else:
    sort_result = SORT some_list STORE cache_sort
    EXPIRE cache_sort 600
    return sort_result
```

SORT是Redis命令最复杂的之一，要注意几点

1. 尽可能减少待排序键中元素的数量
2. 使用LIMIT
3. 尽量使用STORE

## 消息队列

```
BRPOP queue 0

# 优先级任务队列，key1有值先取key1
BRPOP key1 [key2...]
```

发布订阅

```
SUBSCRIBE channel1.1
PUBLISH channel1.1 hi
```

执行SUBSCRIBE命令的客户端会进入订阅状态，此状态下的客户端不能使用除SUBSCRIBE，UNSUBSCRIBE（不指定频道会取消所有订阅），PSUBSCRIBE，PUNSUBSCRIBE之外的命令

```
# channel.?*可以匹配channel1.1、channel1.10等
PSUBSCRIBE channel.?*
```

## 管道

redis-py

```
pipe = r.pipline(transaction=False)
....
result = pipe.execute()


# 事务
pipe = r.pipline()
....
result = pipe.execute()
```