import random, time

class Board:
    def __init__(self, game):
        self.settings = game.settings
        self.board = self._generate_valid_board()
        self.selected = None
        self.game = game

    def _generate_valid_board(self):
        board = []
        for i in range(self.settings.board_height):
            row = []
            for j in range(self.settings.board_width):
                available = [1, 2, 3, 4, 5]
                if j >= 2 and row[j-1] == row[j-2]:
                    if row[j-1] in available:
                        available.remove(row[j-1])
                if i >= 2 and board[i-1][j] == board[i-2][j]:
                    if board[i-1][j] in available:
                        available.remove(board[i-1][j])
                row.append(random.choice(available))
            board.append(row)
        return board

    def _check_eliminate(self):
        eliminated = False
        to_eliminate = set()

        for x in range(self.settings.board_height):
            count = 1
            for y in range(1, self.settings.board_width):
                if self.board[x][y] == self.board[x][y-1] and self.board[x][y] != 0:
                    count += 1
                else:
                    if count >= 3:
                        for i in range(count):
                            to_eliminate.add((x, y-1-i))
                    count = 1
            if count >= 3:
                for i in range(count):
                    to_eliminate.add((x, self.settings.board_width-1-i))

        for y in range(self.settings.board_width):
            count = 1
            for x in range(1, self.settings.board_height):
                if self.board[x][y] == self.board[x-1][y] and self.board[x][y] != 0:
                    count += 1
                else:
                    if count >= 3:
                        for i in range(count):
                            to_eliminate.add((x-1-i, y))
                    count = 1
            if count >= 3:
                for i in range(count):
                    to_eliminate.add((self.settings.board_height-1-i, y))

        if to_eliminate:
            eliminated = True

            for x, y in to_eliminate:
                self.board[x][y] = 0

            self.game._update_screen()
            time.sleep(self.settings.sleep_time)

            self._apply_gravity()

            self.game._update_screen()
            time.sleep(self.settings.sleep_time)

            self._check_eliminate()
        
        return eliminated

    def _apply_gravity(self):
        for y in range(self.settings.board_width):
            write_pos = self.settings.board_height - 1
            for read_pos in range(self.settings.board_height - 1, -1, -1):
                if self.board[read_pos][y] != 0:
                    self.board[write_pos][y] = self.board[read_pos][y]
                    if write_pos != read_pos:
                        self.board[read_pos][y] = 0
                    write_pos -= 1

            for x in range(write_pos + 1):
                self.board[x][y] = random.randint(1, 5)
