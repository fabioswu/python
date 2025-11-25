def hannoi(n, A='A', B='B', C='C'):
    if n == 1:
        print(f'{n}:{A}->{C}')
        return
    hannoi(n-1, A, C, B)
    print(f'{n}:{A}->{C}')
    hannoi(n-1, B, A, C)

hannoi(15)
