class Board:
    def __init__(self, side):
        self.side = side
        self.board = [[(x+1, y+1) for y in range(side)] for x in range(side)]
        self.pos = []
        self.back = [[] for i in range(side)]

    def is_ok(self, a, b, rowIdx):
        return a[1] == b[1] or sum(a) == sum(b) or \
               a[0]-a[1] == b[0]-b[1] or a in self.back[rowIdx]

    def fill(self, rowIdx):
        row = self.board[rowIdx]
        can = []
        if len(self.pos) != 0:
            for i in row:
                ok = True
                for item in self.pos:
                    if self.is_ok(i, item, rowIdx):
                        ok = False
                if ok:
                    can.append(i)
        else:
            can = row
        for i in can:
            if i not in self.back[rowIdx]:
                #print(i)
                self.pos.append(i)
                return True
        return False

    def symmetry_remove(self):
        for i in range(len(self.ans)-1, -1, -1):
            a = []
            for j in self.ans[i]:
                a.append((j[0], self.side+1-j[1]))
            #print(a, self.ans[i], self.side)
            if sorted(a) in self.ans:
                del self.ans[i]
                continue
            a = []
            for j in self.ans[i]:
                a.append((self.side+1-j[0], j[1]))
            #print(a, self.ans[i], self.side)
            if sorted(a) in self.ans:
                del self.ans[i]
                continue
            a = []
            for j in self.ans[i]:
                a.append((j[1], j[0]))
            #print(a, self.ans[i], self.side)
            if sorted(a) in self.ans:
                del self.ans[i]
                continue
            a = []
            for j in self.ans[i]:
                a.append((self.side+1-j[1], self.side+1-j[0]))
            #print(a, self.ans[i], self.side)
            if sorted(a) in self.ans:
                del self.ans[i]
                continue
    
    def rotate_remove(self):
        for i in range(len(self.ans)-1, -1, -1):
            a = []
            for j in self.ans[i]:
                a.append((j[1], self.side+1-j[0]))
            #print(a, self.ans[i], self.side)
            if sorted(a) in self.ans and sorted(a) != self.ans[i]:
                del self.ans[i]
                continue
            a = []
            for j in self.ans[i]:
                a.append((self.side+1-j[0], self.side+1-j[1]))
            #print(a, self.ans[i], self.side)
            if sorted(a) in self.ans and sorted(a) != self.ans[i]:
                del self.ans[i]
                continue
            a = []
            for j in self.ans[i]:
                a.append((self.side+1-j[1], j[0]))
            #print(a, self.ans[i], self.side)
            if sorted(a) in self.ans and sorted(a) != self.ans[i]:
                del self.ans[i]
                continue
    
    def show(self, l):
        a = ''
        for row in range(self.side):
            for line in range(self.side):
                if (row+1, line+1) in l:
                    a += 'Q '
                else:
                    a += '█'
            a += '\n'
        print(a)

    def run(self):
        self.ans = []
        row = 0
        while self.board[0] != self.back[0]:
            suc = self.fill(row)
            if suc:
                row += 1
            else:
                row -= 1
                self.back[row].append(self.pos.pop())
                if row < self.side-1:
                    self.back[row+1] = []
                #print(self.back)
            if row >= self.side:
                row -= 1
                #print(self.pos, self.back)
                self.ans.append(self.pos[:])
                self.back[row].append(self.pos.pop())
                if row < self.side-1:
                    self.back[row+1] = []
        self.symmetry_remove()
        self.rotate_remove()
        for i in self.ans:
            self.show(i)
        print(f'{len(self.ans)} solutions')

a = Board(int(input()))
a.run()
