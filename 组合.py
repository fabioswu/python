def dfs(l, n):
    if n == 1:
        return [[i] for i in l]
    ans = []
    for i in range(1, len(l)-n+2):
        temps = dfs(l[i:], n-1)
        for temp in temps:
            ans.append([l[i-1]]+temp)
    return ans

l = dfs(list(range(1, int(input())+1)), int(input()))
print(l)
