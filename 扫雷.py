import copy

class mineSweeper:
    def __init__(self, board, clicks):
        self.board = board
        self.clicks = clicks

    def try_do(self, x, y):
        if x >= 0 and y >= 0:
            try:
                self.board[x][y]
                return [x, y]
            except:
                return None

    def find_around(self, click):
        x, y = click
        left_up = self.try_do(x-1, y-1)
        up = self.try_do(x-1, y)
        right_up = self.try_do(x-1, y+1)
        left = self.try_do(x, y-1)
        right = self.try_do(x, y+1)
        left_down = self.try_do(x+1, y-1)
        down = self.try_do(x+1, y)
        right_down = self.try_do(x+1, y+1)
        return [a for a in [left_up, left_down, left, up, down,
                            right_down, right_up, right] if a]

    def find_mines(self, poses):
        count = 0
        for x, y in poses:
            if self.board[x][y] == 'M ':
                count += 1
        return count

    def updateBoard(self):
        for x, y in self.clicks:
            if self.board[x][y] == 'M ':
                self.board[x][y] = 'X '
                return
            elif self.board[x][y] == '█':
                around = self.find_around([x, y])
                count = self.find_mines(around)
                #print(around, count)
                if count:
                    self.board[x][y] = str(count)+' '
                else:
                    need_open = []
                    need_treat = [[x, y]]
                    while need_treat:
                        now_treat = need_treat.pop(0)
                        need_open.append(now_treat)
                        around = self.find_around(now_treat)
                        for i in around:
                            count = self.find_mines(self.find_around(i))
                            if i not in need_open:
                                need_open.append(i)
                                if not count:
                                    need_treat.append(i)
                    need_open.sort()
                    for x2, y2 in need_open:
                        around = self.find_around([x2, y2])
                        count = self.find_mines(around)
                        if count:
                            self.board[x2][y2] = str(count)+' '
                        else:
                            self.board[x2][y2] = '□'

    def show(self):
        for i in self.board:
            for j in i:
                if j == 'M ':
                    print('█', end='')
                else:
                    print(j, end='')
            print()

board = [
    ["█","█","█","█","█"],
    ["█","█","M ","█","M "],
    ["█","█","█","█","█"],
    ["█","█","█","█","█"],
    ["█","█","M ","█","█"]
]
clicks = [
    [1, 1]
]
a = mineSweeper(board, clicks)
a.updateBoard()
a.show()
