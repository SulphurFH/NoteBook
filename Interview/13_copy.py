# -*- coding: utf-8 -*-
import copy

print '---------- start copy -----------'
a = [11, 22, 33]
b = [44, 55, 66]
c = [a, b]
d = c
print c
print d
print id(d)
print id(c)
c[0].append(44)
print c
print d
print id(d)
print id(c)
print '---------- end copy -----------'
print '\r\n' * 2
print '---------- start deep copy -----------'
a = [11, 22, 33]
b = [33, 44, 55]
c = [a, b]
e = copy.deepcopy(c)
print c
print e
print id(c)
print id(e)
c[0].append(44)
print c
print e
print id(c)
print id(e)
print '---------- end deep copy -----------'
print '\r\n' * 2
print '---------- start copy.copy -----------'
a = (11, 22, 33, [44, 55])
b = copy.copy(a)
print a
print b
print id(a)
print id(b)
print 'a[3].append(66)'
a[3].append(66)
print a
print b
print id(a)
print id(b)
print id(a[3])
print id(b[3])
print 'a = a + (77, )'
a = a + (77, )
print id(a)
print id(b)
print a
print b
print '---------- end copy.copy -----------'
print '\r\n' * 2
print '---------- start copy.copy -----------'
a = [11, 22, 33, (44, 55)]
b = copy.copy(a)
print a
print b
print id(a)
print id(b)
print 'a.append(66)'
a.append(66)
print a
print b
print id(a)
print id(b)
print '---------- end copy.copy -----------'