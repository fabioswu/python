import re, sys
from collections import deque
class Expression:
    def __init__(self, expr):
        self.expr = expr
        if self.expr[0] == '-':
            self.expr = '0' + self.expr
        print(self.expr)
        self.priority = {'*': 2, '/': 2, '+': 1, '-': 1, '(': 0}
        self.numbers = deque(re.findall(r'\d+\.?\d*', self.expr))
        self.symbols = deque(re.findall(r'[+\-*/\(\)]', self.expr))
        print(self.numbers, self.symbols)
        self.num_stack = deque()
        self.sym_stack = deque()

    def count(self, sym, a, b):
        a = float(a)
        b = float(b)
        if sym == '+':
            return a + b
        if sym == '-':
            return a - b
        if sym == '*':
            return a * b
        if sym == '/':
            if b:
                return a / b
            print('Divide zero error!')
            sys.exit()

    def local_calc(self, rev=False):
        if rev:
            symbol = self.sym_stack.popleft()
            a = self.num_stack.popleft()
            b = self.num_stack.popleft()
            self.num_stack.appendleft(self.count(symbol, a, b))
        else:
            symbol = self.sym_stack.pop()
            b = self.num_stack.pop()
            a = self.num_stack.pop()
            self.num_stack.append(self.count(symbol, a, b))

    def calc(self):
        add = True
        while self.symbols:
            sym = self.symbols.popleft()
            while sym == '(':
                self.sym_stack.append(sym)
                sym = self.symbols.popleft()
            print('0', self.num_stack, self.sym_stack, sym)
            if sym == ')':
                if add:
                    self.num_stack.append(self.numbers.popleft())
                print('1', self.num_stack, self.sym_stack, sym)
                while self.sym_stack[-1] != '(':
                    self.local_calc()
                self.sym_stack.pop()
                print('2', self.num_stack, self.sym_stack, sym)
                add = False
                continue
            if add:
                self.num_stack.append(self.numbers.popleft())
            #print(self.num_stack, self.sym_stack)
            add = True
            if not self.sym_stack or (sym in self.priority.keys() and \
                self.priority[sym] > self.priority[self.sym_stack[-1]]):
                pass
            else:
                #print('a', self.num_stack, self.sym_stack, sym)
                while self.sym_stack and self.priority[self.sym_stack[-1]] >= \
                      self.priority[sym]:
                    self.local_calc()
                    #print(self.num_stack, self.sym_stack, sym)
            self.sym_stack.append(sym)
            print(self.num_stack, self.sym_stack)
        if self.numbers:
            self.num_stack.append(self.numbers.popleft())
        while self.sym_stack:
            #print(self.num_stack, self.sym_stack)
            self.local_calc(rev=True)
        print(self.num_stack[0])

expr = '(((111- 40/6) + 2 +85/5.4 - 2)/(233+5*9)/(10-2*(6-11)) - 10) * 2 - 3'
Expression(expr).calc()
