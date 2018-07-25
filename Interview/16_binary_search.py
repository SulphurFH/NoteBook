# -*- coding: utf-8 -*-


def binary_search(sorted_list, item):
    low = 0
    high = len(sorted_list) + 1
    while low <= high:
        mid = (low + high) / 2
        if sorted_list[mid] > item:
            high = mid - 1
        elif sorted_list[mid] < item:
            low = mid + 1
        else:
            return mid

    return None


mylist = [1, 3, 5, 7, 9]
print binary_search(mylist, 3)
