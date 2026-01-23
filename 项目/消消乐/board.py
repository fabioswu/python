import random, time, copy

class Board:
    def __init__(self, game):
        self.settings = game.settings
        self.board = [[random.randint(1, 5) for _ in range(
            self.settings.board_width)]
            for _ in range(self.settings.board_height)]
        #self.board[5][5] = 0
        #self.board[0][0] = 0
        #self.board[4][5] = 0
        self.selected = None
        self.game = game
        self.sb = game.sb

    def _check_empty(self):
        empty = []
        for x in range(len(self.board)):
            for y in range(len(self.board[0])):
                if self.board[x][y] == 0:
                    empty.append((x, y))
        return empty

    def try_get(self, x, y):
        if x >= 0 and y >= 0:
            try:
                return self.board[x][y]
            except:
                return

    def _check_eliminate(self):
        eliminate_poses = set()
        for x in range(len(self.board)):
            for y in range(len(self.board[0])):
                center = self.board[x][y]
                up_x = x-1
                down_x = x+1
                left_y = y-1
                right_y = y+1
                up = self.try_get(up_x, y)
                down = self.try_get(down_x, y)
                left = self.try_get(x, left_y)
                right = self.try_get(x, right_y)
                if center == up == down:
                    eliminate_poses.add((up_x, y))
                    eliminate_poses.add((x, y))
                    eliminate_poses.add((down_x, y))
                if center == left == right:
                    eliminate_poses.add((x, left_y))
                    eliminate_poses.add((x, y))
                    eliminate_poses.add((x, right_y))
        return eliminate_poses

    def eliminate(self):
        eliminates = self._check_eliminate()
        if eliminates:
            for x, y in eliminates:
                self.board[x][y] = 0
                self.sb.score += 10
            self.update()
            return True

    def update(self):
        self.game._update_screen()
        time.sleep(self.settings.sleep_time)
        empty = self._check_empty()
        if empty:
            for x, y in empty:
                while x > 0:
                    (self.board[x][y], self.board[x-1][y]) = \
                    (self.board[x-1][y], self.board[x][y])
                    x -= 1
                self.board[x][y] = random.randint(1, 5)
            self.update()
        else:
            return self.eliminate()
        return True
