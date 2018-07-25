# coding=utf-8

def qsort(seq):
    if seq == []:
        return []
    else:
        pivot = seq[0]
        lesser = qsort([x for x in seq[1:] if x < pivot])
        greater = qsort([x for x in seq[1:] if x >= pivot])
        return lesser + [pivot] + greater


if __name__ == '__main__':
    seq = [5, 6, 78, 9, 0, -1, 2, 3, -65, 12]
    print(qsort(seq))
