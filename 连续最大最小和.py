class SubList:
    def __init__(self, l, maxormin=True):
        self.l = l
        self.func = max if maxormin else min

    def dfs(self, l):
        if len(l) == 1:
            return l[0]
        mid = len(l) // 2
        left_sum_max = self.dfs(l[:mid])
        right_sum_max = self.dfs(l[mid:])
        left_sum = 0
        right_sum = 0
        left_max = 0
        right_max = 0
        for i in range(mid):
            left_sum += l[mid-i-1]
            right_sum += l[mid+i]
            left_max = self.func(left_sum,left_max)
            right_max = self.func(right_sum, right_max)
        return self.func(left_sum_max, right_sum_max, left_max+right_max)

    def __call__(self):
        return self.dfs(self.l)

print(SubList([1, 2, -3, -4, 7, 9, -1, 4])())
