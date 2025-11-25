import copy
import multiprocessing as mp

class klotski:
    def __init__(self, now, target):
        self.now = now
        self.target = target
        self.visited = [self.now]
        self.now_need = [self.now]
        self.step = {}

    def try_get(self, row, col):
        if row >= 0 and col >= 0:
            try:
                self.now[row][col]
                return (row, col)
            except:
                return None

    def get_around(self, pos):
        up = self.try_get(pos[0]-1, pos[1])
        down = self.try_get(pos[0]+1, pos[1])
        left = self.try_get(pos[0], pos[1]-1)
        right = self.try_get(pos[0], pos[1]+1)
        return [a for a in [up, down, left, right] if a]

    def get_pos(self, board, value):
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == value:
                    return (row, col)

    def exchange(self, pos1, pos2, board):
        (a, b), (c, d) = pos1, pos2
        ret = copy.deepcopy(board)
        ret[a][b], ret[c][d] = ret[c][d], ret[a][b]
        return ret

    def have_solution(self):
        now = copy.deepcopy(self.now)
        times = 0

        for row in range(len(now)):
            for col in range(len(now[row])):
                if now[row][col] != self.target[row][col]:
                    times += 1
                    pos = self.get_pos(now, self.target[row][col])
                    now = self.exchange((row, col), pos, now)

        now_pos = self.get_pos(self.now, 0)
        target_pos = self.get_pos(self.target, 0)
        zero_moves = abs(now_pos[0]-target_pos[0])+abs(now_pos[1]-target_pos[1])
        times += zero_moves
    
        if times % 2 == 0:
            return True
        return False

    def bfs(self):
        self.step[hash(str(self.now))] = None

        while self.now_need:
            need = self.now_need.pop(0)
            pos = self.get_pos(need, 0)
            around = self.get_around(pos)
            for i in around:
                new = self.exchange(pos, i, need)
                if new not in self.visited:
                    self.visited.append(new)
                    self.now_need.append(new)
                    self.step[hash(str(new))] = need
                if new == self.target:
                    print('Find a solution')
                    self.show()
                    return

    def show(self):
        steps = [self.target]
        a = self.step[hash(str(self.target))]
        while a:
            steps.append(a)
            a = self.step[hash(str(a))]
        steps.reverse()
        for i in range(len(steps)):
            print(f'Step {i}:')
            for j in steps[i]:
                for k in j:
                    print(f'{k:>2},', end='')
                print('')

now = [
    [1, 6, 3, 4],
    [5, 2, 12, 8],
    [9, 10, 7, 15],
    [13, 14, 11, 0]
]
target = [
    list(range(1, 5)),
    list(range(5, 9)),
    list(range(9, 13)),
    list(range(13, 16))+[0]
]

if __name__ == '__main__':
    print(target)
    a = klotski(now, target)
    if a.have_solution():
        num_cores = mp.cpu_count()
        print(f'{num_cores} CPU')
        with mp.Pool(processes=num_cores):
            a.bfs()
    else:
        print('No solutions')
