import re, sys
from collections import deque

class Expression:
    def __init__(self, expr):
        if not expr:
            print('None')
            sys.exit(0)
        self.expr = re.sub(r'(?<=^)([+-])', r'0\1',
                           ''.join([i for i in expr if i != ' ']))
        self.expr = re.sub(r'(?<=\()([+-])', r'0\1', self.expr)
        print(self.expr)
        self.priority = {'^': 3, '**': 3, '*': 2, '/': 2, '+': 1,
                         '-': 1, '(': 0}
        self.numbers = deque(re.findall(r'(?<!\d|\))\-?\d+\.?\d*', self.expr))
        self.symbols = deque(re.findall(
            r'[+/\(\)\^]|(?<!\^)\-|(?<!\*)\*{1,2}(?!\*)', self.expr))
        if not self.numbers:
            print('None')
            sys.exit(0)
        print(self.numbers, self.symbols)
        self.num_stack = []
        self.sym_stack = []

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
        if sym in ['^', '**']:
            return a ** b

    def local_calc(self):
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
                self.priority[sym] > self.priority[self.sym_stack[-1]]) or \
                sym in ['^', '**']:
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
        print(self.num_stack, self.sym_stack)
        while self.sym_stack and self.sym_stack[-1] in ['^', '**']:
            self.local_calc()
        while self.sym_stack:
            #print(self.num_stack, self.sym_stack)
            self.local_calc()
        print(self.num_stack[0])

    __call__ = calc

expr = '-(-(-7-9)^(+(-1)))-2^-3'
a = Expression(expr)
a()
