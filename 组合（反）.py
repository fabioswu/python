def dfs(m, n):
    if n == 1:
        return [[i] for i in range(m, 0, -1)]
    ans = []
    for i in range(m, n-1, -1):
        temps = dfs(i-1, n-1)
        for temp in temps:
            ans.append([i]+temp)
    return ans

l = dfs(int(input()), int(input()))
print(l)
