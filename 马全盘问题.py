class Board:
    def __init__(self, m, n, i, j):
        self.board = [[(x, y) for y in range(m)] for x in range(n)]
        self.horse = (i, j)
        self.d = {self.horse: 0}
        self.ret = [[-1 for y in range(m)] for x in range(n)]
        #print(self.ret)
        #print(self.get_around(i, j))

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

    def bfs(self):
        step = 1
        while True:
            cur = {k: v for k, v in self.d.items()}
            for i in cur.keys():
                for j in self.get_around(i[0], i[1]):
                    if j not in self.d.keys():
                        self.d[j] = step
            if self.d == cur:
                break
            step += 1
            #print(self.d)
        #print(self.d)

        for i in self.d.keys():
            self.ret[i[0]][i[1]] = self.d[i]
        self.show()

    def show(self):
        print(f'The horse is on {self.horse}')
        for i in self.ret:
            print(i)

a = Board(50, 50, 2, 3)
a.bfs()
