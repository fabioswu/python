def quick_sort(l):
    if len(l) <= 1:
        return l

    mid = l[0]
    i = 1
    j = len(l)-1
    while True:
        while l[j] > mid:
            j -= 1
        while l[i] <= mid and i < j:
            i += 1
        if i < j:
            l[i], l[j] = l[j], l[i]
        else:
            l[0], l[j] = l[j], l[0]
            break

    l[:j] = quick_sort(l[:j])
    l[j+1:] = quick_sort(l[j+1:])

    return l

l = [44, 37, 92, 44, 71, 59, 23, 59, 12, 68, 44, 27, 4, 53, 88, 19, 19, 27, 71]
print(quick_sort(l))
