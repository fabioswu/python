class Expression:
    def __init__(self, expr):
        self.tokens = []
        i = 0
        n = len(expr)
        while i < n:
            if expr[i] == ' ':
                i += 1
                continue

            if expr[i] == '-' and (i == 0 or self.tokens and
                                   self.tokens[-1] in '(+-*/^'):
                i += 1
                num = '-'
                while i < n and (expr[i].isdigit() or expr[i] == '.'):
                    num += expr[i]
                    i += 1
                if len(num) > 1:
                    self.tokens.append(num)
                else:
                    self.tokens += ['0', '-']

            elif expr[i] == '+' and (i == 0 or self.tokens and
                                   self.tokens[-1] in '(+-*/^'):
                i += 1
                num = '+'
                while i < n and (expr[i].isdigit() or expr[i] == '.'):
                    num += expr[i]
                    i += 1
                if len(num) > 1:
                    self.tokens.append(num)
                else:
                    self.tokens += ['0', '+']

            elif expr[i].isdigit() or expr[i] == '.':
                num = ''
                while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                    num += expr[i]
                    i += 1
                self.tokens.append(num)

            elif expr[i] in '()+-*/^':
                self.tokens.append(expr[i])
                i += 1

    def parse(self):
        self.output = []
        operators = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        
        for token in self.tokens:
            if token.replace('.', '').replace('-', '').replace('+', '').isdigit():
                self.output.append(float(token) if '.' in token else int(token))

            elif token in precedence.keys():
                while (operators and operators[-1] != '(' and
                       precedence[operators[-1]] >= precedence[token]):
                    self.output.append(operators.pop())
                operators.append(token)

            elif token == '(':
                operators.append(token)

            elif token == ')':
                while operators[-1] != '(':
                    self.output.append(operators.pop())
                operators.pop()
        
        while operators:
            self.output.append(operators.pop())

    def calc(self):
        self.parse()
        stack = []
        for token in self.output:
            if isinstance(token, (int, float)):
                stack.append(token)
            else:
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b)
                elif token == '^':
                    stack.append(a ** b)
        self.ans = stack[0]

a = Expression('+1-(+(-(-2)))')
print(a.tokens)
a.calc()
print(a.output)
print(a.ans)
