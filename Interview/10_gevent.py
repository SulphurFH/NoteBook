# -*- coding: utf-8 -*-

import urllib2
import gevent
from gevent import monkey

monkey.patch_all()


def myDownLoad(url):
    print('GET: %s' % url)
    resp = urllib2.urlopen(url)
    data = resp.read()
    print('%d bytes received from %s.' % (len(data), url))


gevent.joinall([
    gevent.spawn(myDownLoad, 'http://www.baidu.com/'),
    gevent.spawn(myDownLoad, 'http://www.itheima.com/'),
    gevent.spawn(myDownLoad, 'http://www.itcast.cn/'),
])
