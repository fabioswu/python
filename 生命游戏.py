import random, time

class Board:
    def __init__(self, side):
        self.side = side
        self.renew()
        temp = []
        self.board = []
        for i in range(side):
            self.board.append(temp[:])
        for y in range(side):
            for x in range(side):
                a = random.randint(0, 2)
                if a == 2:
                    self.board[y].append(1)
                else:
                    self.board[y].append(0)
        self.last_board = self.empty_board[:]
        #print(self.last_board)
        '''
        self.board = self.empty_board[:]
        self.board[0][1] = 1
        self.board[1][2] = 1
        self.board[2][0] = 1
        self.board[2][1] = 1
        self.board[2][2] = 1
        self.renew()
        self.last_board = self.empty_board[:]
        '''
        #print(self.board)

    def renew(self):
        temp = [0]*self.side
        self.empty_board = []
        for i in range(self.side):
            self.empty_board.append(temp[:])

    def try_do(self, y, x):
        if y<0 or x<0:
            return 0
        try:
            return self.board[y][x]
        except:
            return 0

    def sum_around(self, y, x):
        up = self.try_do(y-1, x)
        down = self.try_do(y+1, x)
        left = self.try_do(y, x-1)
        right = self.try_do(y, x+1)
        up_left = self.try_do(y-1, x-1)
        up_right = self.try_do(y-1, x+1)
        down_left = self.try_do(y+1, x-1)
        down_right = self.try_do(y+1, x+1)
        #print([y, x], [up_left, up, up_right, left, right, down_left, down, down_right])
        return sum([up_left, up, up_right, left, right, down_left, down, down_right])

    def next_step(self):
        self.renew()
        #print(self.empty_board)
        new_board = self.empty_board[:]
        birth = [3, ]
        stay = [2, 3, ]
        for y in range(self.side):
            for x in range(self.side):
                if (self.board[y][x] == 0 and self.sum_around(y, x) in birth) or \
                   (self.board[y][x] == 1 and (self.sum_around(y, x) in stay)):
                    new_board[y][x] = 1
        self.board = new_board

    def break_(self):
        if self.board == self.empty_board or self.board == self.last_board:
            #print(self.board, self.empty_board, self.last_board, sep='\n\n')
            return True
        return False

    def show(self):
        a = ''
        for i in self.board:
            for j in i:
                if j == 1:
                    a += '█'
                if j == 0:
                    a += '  '
            a += '\n'
        print(a)
        print('-'*(self.side*2+1))

    def run(self):
        while True:
            self.renew()
            self.show()
            if self.break_():
                break
            self.last_board = self.board[:]
            self.next_step()
            time.sleep(1)

a = Board(int(input()))
a.run()
