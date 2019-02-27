# Redis

## Redis Cluster

### Redis Cluster介绍

[cluster-tutorial](http://www.redis.cn/topics/cluster-tutorial.html) 

### Redlis Cluster客户端介绍

[Grokzen/redis-py-cluster](https://github.com/Grokzen/redis-py-cluster)

### Redis Cluster官方规范

[原文](https://github.com/antirez/redis-doc/blob/master/topics/cluster-spec.md)

[译文](http://ifeve.com/redis-cluster-spec/)

Keys hash tags

Redis Cluster implements all the single key commands available in the non-distributed version of Redis. Commands performing complex multi-key operations like Set type unions or intersections are implemented as well as long as the keys all belong to the same node.

实现键哈希标签(注意并不能区分key)

哈希标签是确保两个键都在同一个哈希槽里的一种方式

使用哈希标签，用户可以自由地使用多键操作
Multi-key operations may become unavailable when a resharding of the hash slot the keys belong to is in progress.