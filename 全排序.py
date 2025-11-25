def all_sorts(ans, back, n):
    for i in range(1, n+1):
        if str(i) not in back:
            back += str(i)
            if len(back) == n:
                ans.append(back)
                back = back[:-1]
                return
            all_sorts(ans, back, n)
            back = back[:-1]

ans = []
n = 4
all_sorts(ans, '', n)
print(ans)
