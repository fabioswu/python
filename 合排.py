def merge_sort(l):
    if len(l) <= 1:
        return l

    mid = len(l) // 2
    left = l[:mid]
    right = l[mid:]

    left = merge_sort(left)
    right = merge_sort(right)
    result = []
    while left and right:
        if left[0] < right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result += left
    result += right

    return result

l = [44, 37, 92, 44, 71, 59, 23, 59, 12, 68, 44, 27, 4, 53, 88, 19, 19, 27, 71]
print(merge_sort(l))
