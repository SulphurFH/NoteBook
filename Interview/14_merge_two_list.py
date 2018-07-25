# -*- coding: utf-8 -*-

l1 = [1, 2, 3, 7]
l2 = [3, 4, 5]


def _recursion_merge_sort2(l1, l2, tmp):
    if len(l1) == 0 or len(l2) == 0:
        tmp.extend(l1)
        tmp.extend(l2)
        return tmp
    else:
        if l1[0] < l2[0]:
            tmp.append(l1[0])
            del l1[0]
        else:
            tmp.append(l2[0])
            del l2[0]
        return _recursion_merge_sort2(l1, l2, tmp)


def recursion_merge_sort2(l1, l2):
    return _recursion_merge_sort2(l1, l2, [])


def merge_sortedlist(l1, l2):
    l3 = []
    while l1 and l2:
        if l1[0] >= l2[0]:
            l3.append(l2.pop(0))
        else:
            l3.append(l1.pop(0))
    while l1:
        l3.append(l1.pop(0))
    while l2:
        l3.append(l2.pop(0))
    return l3


def loop_merge_sort(l1, l2):
    tmp = []
    while len(l1) > 0 and len(l2) > 0:
        if l1[0] < l2[0]:
            tmp.append(l1[0])
            del l1[0]
        else:
            tmp.append(l2[0])
            del l2[0]
    tmp.extend(l1)
    tmp.extend(l2)
    return tmp


if __name__ == "__main__":
    print recursion_merge_sort2(l1, l2)
    # print merge_sortedlist(l1, l2)
    # print loop_merge_sort(l1, l2)
