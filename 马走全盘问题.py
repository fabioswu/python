import copy

class Board:
    def __init__(self, m, n, x, y):
        self.board = [[(x, y) for y in range(m)] for x in range(n)]
        self.num = m * n
        self.cur = (x, y)
        self.back = [self.cur]
        self.ret = [[-1 for y in range(m)] for x in range(n)]
        self.step = 1
        self.ret[x][y] = 0
        self.anss = []
        self.dfs(x, y)
        print(f'The horse is on {self.cur}')
        for ans in self.anss:
            self.show(ans)
            print('---------------')
        print(f'{len(self.anss)} solutions')

    def try_do(self, x, y):
        if x >= 0 and y >= 0:
            try:
                return self.board[x][y]
            except Exception:
                return

    def get_around(self, x, y):
        up_left = self.try_do(x-2, y-1)
        up_right = self.try_do(x-2, y+1)
        left_up = self.try_do(x-1, y-2)
        right_up = self.try_do(x-1, y+2)
        left_down = self.try_do(x+1, y-2)
        right_down = self.try_do(x+1, y+2)
        down_left = self.try_do(x+2, y-1)
        down_right = self.try_do(x+2, y+1)
        ret = [up_left, up_right, left_up, right_up, left_down, right_down,\
               down_left, down_right]
        return [i for i in ret if i]

    def dfs(self, x, y):
        for i in self.get_around(x, y):
            if i not in self.back:
                self.ret[i[0]][i[1]] = self.step
                self.step += 1
                self.back.append(i)
                print(self.back)
                if len(self.back) == self.num:
                    self.anss.append(copy.deepcopy(self.ret))
                    self.step -= 1
                    self.back.pop()
                    self.ret[i[0]][i[1]] = -1
                    return
                self.dfs(i[0], i[1])
                self.step -= 1
                self.back.pop()
                self.ret[i[0]][i[1]] = -1

    def show(self, l):
        for i in l:
            for j in i:
                print('%2d' % j, end=' ')
            print('')

Board(5, 5, 2, 2)
