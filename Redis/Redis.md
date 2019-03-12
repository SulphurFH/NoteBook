# Redis设计与实现

## 简单动态字符串（SDS）

### SDS区别C字符串

* SDS包括三部分（free，len，buf）, STRLEN的复杂度为O(1)，C字符串为O(n)

* 杜绝缓冲区溢出

* SDS通过未使用空间解除字符串长度和底层数组长度之间的关联, buf = 字符串数量 + 1 + free，达到空间预分配和惰性空间释放

* 空间预分配：用于字符串增加, SDS修改后的len<1MB，设置free=len，buf=len+free+1; len>1MB, free=1MB, buf=len+1MB(free)+1byte

* 惰性空间释放：用于字符串减少，修改了len与free之后，buf不会释放出多余的字节空间，为将来字符串增加做优化
