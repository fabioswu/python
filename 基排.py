def radix_sort(l):
    length = len(str(max(l)))
    for i in range(length):
        buckets = [[] for a in range(10)]
        for j in l:
            buckets[(j//(10**i)) % 10].append(j)
        l.clear()
        for x in buckets:
            l += x

l = [44, 37, 92, 44, 71, 59, 23, 59, 12, 68, 44, 27, 4, 53, 88, 19, 19, 27, 71]
radix_sort(l)
print(l)
