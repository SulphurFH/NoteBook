# -*- coding: utf-8 -*-


def quicksort(chaotic_list):
    if len(chaotic_list) < 2:
        return chaotic_list
    else:
        midpivot = chaotic_list[0]
        lessbeforemidpivot = quicksort([i for i in chaotic_list[1:] if i < midpivot])
        biggerafterpivot = quicksort([i for i in chaotic_list[1:] if i > midpivot])
        return lessbeforemidpivot + [midpivot] + biggerafterpivot


print quicksort([2, 4, 6, 7, 1, 2, 5])
