import re
from collections import deque

class Expression:
    def __init__(self, expr):
        if not expr:
            return 'None'
        self.expr = ''.join([i for i in expr if i != ' '])
        # 判断开头是否为正负号
        first = False
        if self.expr[0] in ['-', '+']:
            first = True
            self.expr = '(0'+self.expr
        # 把(-x)变成(0-x)
        self.expr = re.sub(r'(?<=\()([+-])', r'0\1', self.expr)
        #print(self.expr)
        self.priority = {'^': 3, '**': 3, '*': 2, '/': 2,
                         '//': 2, '+': 1, '-': 1, '(': 0}
        # 提取数字
        self.numbers = deque(re.findall(r'(?<!\d|\))\-?\d+\.?\d*', self.expr))
        # 提取符号
        self.symbols = deque(re.findall(
            r'[+\(\)\^]|(?<!\^)\-|(?<!\*)\*{1,2}(?!\*)|(?<!/)/{1,2}(?!/)',
            self.expr))
        # 若开头加0，则强制添加括号
        if first:
            self.symbols.insert(2, ')')
        if not self.numbers:
            return 'None'
        #print(self.numbers, self.symbols)
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
            return f'{a} / {b} is not supported!'
        if sym in ['^', '**']:
            if (a == 0 and b <= 0) or (a < 0 and int(b) != b):
                return f'{a} ** {b} is not supported!'
            return a ** b
        if sym == '//':
            if b:
                return a // b
            return f'{a} // {b} is not supported!'

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
            #print('0', self.num_stack, self.sym_stack, sym)
            if sym == ')':
                if add:
                    self.num_stack.append(self.numbers.popleft())
                #print('1', self.num_stack, self.sym_stack, sym)
                while self.sym_stack[-1] != '(':
                    self.local_calc()
                self.sym_stack.pop()
                #print('2', self.num_stack, self.sym_stack, sym)
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
            #print(self.num_stack, self.sym_stack)
        if self.numbers:
            self.num_stack.append(self.numbers.popleft())
        #print(self.num_stack, self.sym_stack)
        while self.sym_stack and self.sym_stack[-1] in ['^', '**']:
            self.local_calc()
        while self.sym_stack:
            #print(self.num_stack, self.sym_stack)
            self.local_calc()
        return self.num_stack[0]

    __call__ = calc

expr = '2^(1/2)'
a = Expression(expr)
print(a())
