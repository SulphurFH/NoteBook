LIMIT = 5


def pairs(seq):
    n = len(seq)
    for i in range(n):
        yield seq[i], seq[(i + 1) % n]


def allUniqueSort(s):
    print('allUniqueSort')
    strStr = sorted(s)
    for (c1, c2) in pairs(strStr):
        if c1 == c2:
            return False
    return True


def allUniqueSet(s):
    print('allUniqueSet')
    return True if len(set(s)) == len(s) else False


def allUnique(s, strategy):
    return strategy(s)


def main():
    while True:
        word = None
        while not word:
            word = input('Insert word (type quit to exit)> ')
            if word == 'quit':
                print('bye')
                return
        word_len = len(word)
        strategy = allUniqueSet if word_len < LIMIT else allUniqueSort
        print('allUnique({}): {}'.format(word, allUnique(word, strategy)))
        print()


if __name__ == "__main__":
    main()
