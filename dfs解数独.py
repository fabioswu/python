class Board:
    def __init__(self, board):
        self.board = board
        #print(self.board)

    def is_ok(self, x, y, value):
        for i in range(9):
            if value in [self.board[x][i], self.board[i][y]]:
                return False

        start_x, start_y = 3 * (x//3), 3 * (y//3)
        for i in range(3):
            for j in range(3):
                if self.board[start_x+i][start_y+j] == value:
                    return False

        return True

    def fill(self, start_x=0, start_y=0):
        for x in range(start_x, 9):
            for y in range(9) if x != start_x else range(start_y, 9):
                if self.board[x][y] == 0:
                    for i in range(1, 10):
                        if self.is_ok(x, y, i):
                            self.board[x][y] = i
                            '''
                            self.show()
                            print('')
                            '''
                            if self.fill(x, y):
                                return True
                            self.board[x][y] = 0
                            '''
                            self.show()
                            print('')
                            '''
                    return False
        return True

    def show(self):
        for i in self.board:
            print(i)

    def solve(self):
        if self.fill():
            self.show()
        else:
            print('Fail to solve')

a = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 3, 6, 0, 0, 0, 0, 0],
     [0, 7, 0, 0, 9, 0, 2, 0, 0],
     [0, 5, 0, 0, 0, 7, 0, 0, 0],
     [0, 0, 0, 0, 4, 5, 7, 0, 0],
     [0, 0, 0, 1, 0, 0, 0, 3, 0],
     [0, 0, 1, 0, 0, 0, 0, 6, 8],
     [0, 0, 8, 5, 0, 0, 0, 1, 0],
     [0, 9, 0, 0, 0, 0, 4, 0, 0]
]
a = Board(a)
a.solve()
