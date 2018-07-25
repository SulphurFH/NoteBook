# -*- coding: utf-8 -*-

filter_func = filter(lambda x: x > 5, [i for i in range(11)])
map_func = map(lambda x: x * 2, [i for i in range(11)])
reduce_func = reduce(lambda x, y: x + y, [i for i in range(11)])

if __name__ == "__main__":
    print filter_func
    print map_func
    print reduce_func
