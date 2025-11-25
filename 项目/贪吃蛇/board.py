import random

class Board:
    def __init__(self, snake_game):
        self.settings = snake_game.settings
        self.board_height = self.settings.board_height
        self.board_width = self.settings.board_width
        self.board = [[0 for _ in range(self.board_width)]
                      for _ in range(self.board_height)]
        self.board[0][0] = 4
        self.head_pos = [0, 0]
        self.tail_pos = [0, 0]
        self.direction = 2
        self.stats = snake_game.stats
        self.food_pos = [0, 0]

    def update_snake(self):
        x, y = self.head_pos

        if self.direction == 1:
            self.board[x][y] = 3
            if x-1 < 0:
                x = self.board_height - 1
            else:
                x -= 1
        elif self.direction == 2:
            self.board[x][y] = 4
            if y+1 >= self.board_width:
                y = 0
            else:
                y += 1
        elif self.direction == 3:
            self.board[x][y] = 1
            if x+1 >= self.board_height:
                x = 0
            else:
                x += 1
        elif self.direction == 4:
            self.board[x][y] = 2
            if y-1 < 0:
                y = self.board_width - 1
            else:
                y -= 1

        if self.board[x][y] in [1, 2, 3, 4]:
            return True
        if not self._is_eating_food([x, y]):
            self._update_tail()
        else:
            self.stats.score += 1
            self.give_food()

        if self.direction == 1:
            self.board[x][y] = 3
        elif self.direction == 2:
            self.board[x][y] = 4
        elif self.direction == 3:
            self.board[x][y] = 1
        elif self.direction == 4:
            self.board[x][y] = 2
            
        self.head_pos = [x, y]

    def _update_tail(self):
        x, y = self.tail_pos
        tail = self.board[x][y]
        self.board[x][y] = 0

        if tail == 1:
            if x+1 >= self.board_height:
                x = 0
            else:
                x += 1

        elif tail == 2:
            if y-1 < 0:
                y = self.board_width - 1
            else:
                y -= 1

        elif tail == 3:
            if x-1 < 0:
                x = self.board_height - 1
            else:
                x -= 1

        elif tail == 4:
            if y+1 >= self.board_width:
                y = 0
            else:
                y += 1

        self.tail_pos = [x, y]

    def give_food(self):
        x, y = (random.randint(0, self.settings.board_height-1),
                random.randint(0, self.settings.board_width-1))
        while self.board[x][y] != 0:
            x, y = (random.randint(0, self.settings.board_height-1),
                    random.randint(0, self.settings.board_width-1))
        self.board[x][y] = 5
        self.food_pos = [x, y]

    def _is_eating_food(self, pos):
        return pos == self.food_pos
