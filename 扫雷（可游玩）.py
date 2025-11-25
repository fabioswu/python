import random

class mineSweeper:
    def __init__(self, board, copy_board):
        self.board = board
        self.copy_board = copy_board

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
            if self.board[x][y] in ['M ', '※']:
                count += 1
        return count

    def find_flags(self, poses):
        count = 0
        for x, y in poses:
            if self.board[x][y] == '※':
                count += 1
        return count

    def updateBoard(self, clicks):
        x, y = clicks
        if self.board[x][y] == 'M ':
            self.board[x][y] = 'X '
            return True
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
        elif self.board[x][y][0].isdigit():
            around = self.find_around([x, y])
            count = self.find_flags(around)
            #print(around, count)
            if count == int(self.board[x][y]):
                go = False
                for x1, y1 in around:
                    if self.board[x1][y1] in ['█', 'M ']:
                        #print(x1, y1)
                        a = self.updateBoard([x1, y1])
                        if a:
                            go = True
                if go:
                    return True

    def show(self):
        print(end='    ')
        for i in range(len(self.board[0])):
            print(f'{i:<2}', end='')
        print('\n  ┌', end='')
        for i in range(len(self.board[0])):
            print('─', end='')
        print('┐')
        for i in range(len(self.board)):
            print(f'{i:<2}', end='│')
            for j in self.board[i]:
                if j == 'M ':
                    print('█', end='')
                else:
                    print(j, end='')
            print(f'│{i:<2}')
        print('  └', end='')
        for i in range(len(self.board[0])):
            print('─', end='')
        print('┘\n    ', end='')
        for i in range(len(self.board[0])):
            print(f'{i:<2}', end='')
        print()

    def is_all_ok(self):
        for i in self.board:
            if '█' in i:
                return False
        return True

    def run(self):
        lose = False
        while not self.is_all_ok():
            self.show()
            inp = input().split()
            click = []
            if len(inp) not in [2, 3]:
                print('\n输入有误，请重输\n')
                continue
            else:
                try:
                    if int(inp[0]) >= 0 and int(inp[1]) >= 0:
                        self.board[int(inp[0])][int(inp[1])]
                except:
                    print('\n输入有误，请重输\n')
                    continue
            if len(inp) == 2:
                click_type = 0
                for i in inp:
                    click.append(int(i))
            else:
                click_type = 1
                for i in inp[:2]:
                    click.append(int(i))
            if click_type:
                x, y = click
                if self.board[x][y] in ['M ', '█']:
                    self.board[x][y] = '※'
                elif self.board[x][y] == '※':
                    self.board[x][y] = '? '
                elif self.board[x][y] == '? ':
                    self.board[x][y] = self.copy_board[x][y]
            else:
                lose = self.updateBoard(click)
                if lose:
                    break
            #print(board)
        self.show()
        if lose:
            print('\nYou lose!\n')
        else:
            print('\nYou win!\n')
        self.show_all_mines(lose)

    def show_all_mines(self, lose):
        print('All mines are:')
        print(end='    ')
        for i in range(len(self.board[0])):
            print(f'{i:<2}', end='')
        print('\n  ┌', end='')
        for i in range(len(self.board[0])):
            print('─', end='')
        print('┐')
        for i in range(len(self.board)):
            print(f'{i:<2}│', end='')
            for j in range(len(self.copy_board[i])):
                '''
                屎，但是也可以用
                print((('M ' if self.board[i][j] == '※' else 'X ')
                      if self.copy_board[i][j] == 'M ' else
                      self.copy_board[i][j]), end='')
                '''
                if self.copy_board[i][j] == 'M ':
                    if self.board[i][j] == '※' or not lose:
                        print('M ', end='')
                    else:
                        print('X ', end='')
                else:
                    print(self.copy_board[i][j], end='')
            print(f'│{i:<2}')
        print('  └', end='')
        for i in range(len(self.board[0])):
            print('─', end='')
        print('┘')
        print(end='    ')
        for i in range(len(self.board[0])):
            print(f'{i:<2}', end='')
        print()

length = 8
width = 8
board = [["█" for _ in range(length)] for _ in range(width)]
copy_board = [["█" for _ in range(length)] for _ in range(width)]
counts = int(length*width/5)
#counts = 100
#counts = 1
for i in range(counts):
    a, b = random.randint(0, width-1), random.randint(0, length-1)
    board[a][b] = 'M '
    copy_board[a][b] = 'M '
a = mineSweeper(board, copy_board)
a.run()
