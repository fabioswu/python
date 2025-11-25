import copy
import multiprocessing as mp
from collections import deque
import time
import hashlib

class klotski:
    def __init__(self, now, target):
        self.now = now
        self.target = target
        self.visited = set()
        self.visited.add(self.board_to_str(now))
        self.queue = deque([(now, 0)])
        self.step = {}
        self.found = False

    def board_to_str(self, board):
        """将棋盘转换为字符串，便于哈希和比较"""
        return ''.join(str(cell) for row in board for cell in row)

    def board_to_hash(self, board):
        """使用更紧凑的哈希表示"""
        return hashlib.md5(self.board_to_str(board).encode()).hexdigest()

    def try_get(self, row, col, board):
        if 0 <= row < len(board) and 0 <= col < len(board[0]):
            return (row, col)
        return None

    def get_around(self, pos, board):
        up = self.try_get(pos[0]-1, pos[1], board)
        down = self.try_get(pos[0]+1, pos[1], board)
        left = self.try_get(pos[0], pos[1]-1, board)
        right = self.try_get(pos[0], pos[1]+1, board)
        return [a for a in [up, down, left, right] if a]

    def get_pos(self, board, value):
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == value:
                    return (row, col)
        return None

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
                    if pos:
                        now = self.exchange((row, col), pos, now)

        now_pos = self.get_pos(self.now, 0)
        target_pos = self.get_pos(self.target, 0)
        if now_pos and target_pos:
            zero_moves = abs(now_pos[0]-target_pos[0])+abs(now_pos[1]-target_pos[1])
            times += zero_moves
    
        return times % 2 == 0

    def expand_batch(self, boards_batch):
        """批量扩展多个棋盘状态"""
        results = []
        for board in boards_batch:
            pos = self.get_pos(board, 0)
            if not pos:
                continue
                
            around = self.get_around(pos, board)
            for new_pos in around:
                new_board = self.exchange(pos, new_pos, board)
                board_str = self.board_to_str(new_board)
                results.append((new_board, board_str, board))
        return results

def parallel_bfs_worker(initial_boards, target, max_depth=50, batch_size=1000):
    """独立的工作进程函数，不依赖类实例"""
    def board_to_str(board):
        return ''.join(str(cell) for row in board for cell in row)
    
    def get_pos(board, value):
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == value:
                    return (row, col)
        return None
    
    def try_get(row, col, board):
        if 0 <= row < len(board) and 0 <= col < len(board[0]):
            return (row, col)
        return None
    
    def get_around(pos, board):
        up = try_get(pos[0]-1, pos[1], board)
        down = try_get(pos[0]+1, pos[1], board)
        left = try_get(pos[0], pos[1]-1, board)
        right = try_get(pos[0], pos[1]+1, board)
        return [a for a in [up, down, left, right] if a]
    
    def exchange(pos1, pos2, board):
        (a, b), (c, d) = pos1, pos2
        ret = copy.deepcopy(board)
        ret[a][b], ret[c][d] = ret[c][d], ret[a][b]
        return ret
    
    # 工作进程本地的数据结构
    visited = set()
    queue = deque()
    step = {}
    
    # 初始化
    for board in initial_boards:
        board_str = board_to_str(board)
        visited.add(board_str)
        step[board_str] = None
        queue.append((board, 0))
    
    depth_states = 0
    max_states_per_depth = batch_size
    
    while queue:
        current, depth = queue.popleft()
        
        # 检查是否找到目标
        if current == target:
            return ('found', current, depth, step)
        
        # 限制搜索深度和每层状态数
        if depth > max_depth or depth_states > max_states_per_depth:
            continue
        
        pos = get_pos(current, 0)
        if not pos:
            continue
            
        around = get_around(pos, current)
        for new_pos in around:
            new_board = exchange(pos, new_pos, current)
            board_str = board_to_str(new_board)
            
            if board_str not in visited:
                visited.add(board_str)
                queue.append((new_board, depth + 1))
                step[board_str] = current
                depth_states += 1
    
    # 返回本进程发现的新状态
    return ('partial', list(queue), visited, step)

def parallel_bfs_main(now, target):
    """主并行BFS函数"""
    if not klotski(now, target).have_solution():
        print('No solutions')
        return None

    num_cores = mp.cpu_count()
    print(f'Using {num_cores} CPU cores for parallel BFS')
    
    # 创建进程池
    with mp.Pool(processes=num_cores) as pool:
        # 初始批次：从不同方向开始搜索
        initial_batches = []
        batch_size = 100
        
        # 创建多个不同的初始批次
        for i in range(num_cores):
            initial_batches.append([now])  # 每个进程从相同状态开始但可能探索不同路径
        
        results = []
        for batch in initial_batches:
            result = pool.apply_async(parallel_bfs_worker, (batch, target, 30, 500))
            results.append(result)
        
        # 收集结果
        for i, result in enumerate(results):
            try:
                worker_result = result.get(timeout=30)  # 30秒超时
                if worker_result[0] == 'found':
                    print(f"Worker {i} found solution!")
                    return worker_result
            except mp.TimeoutError:
                print(f"Worker {i} timed out")
            except Exception as e:
                print(f"Worker {i} error: {e}")
    
    print("No solution found by any worker")
    return None

def reconstruct_path(final_board, step_dict, board_to_str):
    """重构解决方案路径"""
    path = []
    current = final_board
    
    while current is not None:
        path.append(current)
        current_str = board_to_str(current)
        current = step_dict.get(current_str)
    
    path.reverse()
    return path

def show_solution(path):
    """显示解决方案"""
    print(f"Solution found in {len(path)-1} steps:")
    for i, step in enumerate(path):
        print(f'Step {i}:')
        for row in step:
            for cell in row:
                print(f'{cell:>2},', end='')
            print()
        print()

# 原有的单进程BFS（保持原样）
def original_bfs(now, target):
    """使用原有的单进程BFS算法"""
    solver = klotski(now, target)
    if not solver.have_solution():
        print('No solutions')
        return
    
    solver.step[solver.board_to_str(solver.now)] = None
    
    while solver.queue and not solver.found:
        current, depth = solver.queue.popleft()
        
        if current == target:
            print(f'Find a solution in {depth} steps')
            solver.found = True
            # 重构路径
            path = reconstruct_path(current, solver.step, solver.board_to_str)
            show_solution(path)
            return
        
        pos = solver.get_pos(current, 0)
        around = solver.get_around(pos, current)
        
        for new_pos in around:
            new_board = solver.exchange(pos, new_pos, current)
            board_str = solver.board_to_str(new_board)
            
            if board_str not in solver.visited:
                solver.visited.add(board_str)
                solver.queue.append((new_board, depth + 1))
                solver.step[board_str] = current
        '''
        if depth % 10 == 0:
            print(f'Depth: {depth}, Queue size: {len(solver.queue)}, '
                  f'Visited: {len(solver.visited)}')
        '''

# 测试代码
if __name__ == '__main__':
    now = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 12, 11],
        [13, 15, 14, 0]
    ]
    target = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]

    print("Target state:")
    for row in target:
        print(row)

    print("\nSearching for solution...")
    
    # 方法1：使用并行BFS
    start_time = time.time()
    result = parallel_bfs_main(now, target)
    end_time = time.time()
    
    if result and result[0] == 'found':
        _, solution_board, steps, step_dict = result
        path = reconstruct_path(solution_board, step_dict, 
                              lambda b: ''.join(str(cell) for row in b for cell in row))
        show_solution(path)
    else:
        print("Parallel BFS didn't find solution, trying single process...")
        # 方法2：回退到单进程BFS
        original_bfs(now, target)
    
    print(f"Search completed in {end_time - start_time:.2f} seconds")
