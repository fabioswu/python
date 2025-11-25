class LongDivide:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.ans = ''

    def div(self):
        if self.b == 0:
            return 'Divide by zero!'
        if (self.a < 0 and self.b > 0) or (self.a > 0 and self.b < 0):
            self.ans += '-'
        if '.' in str(self.b):
            length = len(str(self.b).split('.')[-1])
            self.a *= 10**length
            self.b *= 10**length
        if 'e' in str(self.b):
            return 'Divisor is too small!'
        self.a = abs(self.a)
        self.b = abs(self.b)
        self.ans += str(self.a // self.b)
        self.a %= self.b
        fraction = ''
        visited = []
        if self.a:
            self.ans += '.'
            while self.a:
                visited.append(self.a)
                self.a *= 10
                fraction += str(self.a//self.b)
                self.a %= self.b
                for i in range(len(visited)):
                    if visited[i] == self.a:
                        self.ans += fraction[:i]
                        self.ans += '('+fraction[i:]+')'
                        return self.ans, visited
        return self.ans+fraction, visited

    def __call__(self):
        return self.div()

print(LongDivide(8, -0.00000000000000000000000000000114)())
print(LongDivide(11974, 11973)())
