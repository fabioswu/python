import pygame
import random
import os
import copy

pygame.init()

GRID_WIDTH = 20
GRID_NUM_WIDTH = 15
GRID_NUM_HEIGHT = 25
WIDTH, HEIGHT = GRID_WIDTH * GRID_NUM_WIDTH, GRID_WIDTH * GRID_NUM_HEIGHT
SIDE_WIDTH = 200
SCREEN_WIDTH = WIDTH + SIDE_WIDTH
WHITE = (0xff, 0xff, 0xff)
BLACK = (0, 0, 0)
LINE_COLOR = (0x33, 0x33, 0x33)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 120, 255)

CUBE_COLORS = [
    (0xcc, 0x99, 0x99), (0xff, 0xff, 0x99), (0x66, 0x66, 0x99),
    (0x99, 0x00, 0x66), (0xff, 0xcc, 0x00), (0xcc, 0x00, 0x33),
    (0xff, 0x00, 0x33), (0x00, 0x66, 0x99), (0xff, 0xff, 0x33),
    (0x99, 0x00, 0x33), (0xcc, 0xff, 0x66), (0xff, 0x99, 0x00)
]

screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT))
pygame.display.set_caption("俄罗斯方块 - 自动模式")
clock = pygame.time.Clock()
FPS = 30

score = 0
level = 1
lineCount = [0,0,0,0]
auto_mode = False  # 自动模式开关
auto_move_counter = 0
auto_move_interval = 5  # 自动移动间隔帧数
best_move_path = []  # 存储最佳移动路径

screen_color_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]

# 设置游戏的根目录为当前文件夹
base_folder = os.path.dirname(__file__)


def show_text(surf, text, size, x, y, color=WHITE):
    font_name = os.path.join(base_folder, '方圆体.ttc')
    try:
        font = pygame.font.Font(font_name, size)
    except:
        font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class CubeShape(object):
    SHAPES = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
    I = [[(0, -1), (0, 0), (0, 1), (0, 2)],
         [(-1, 0), (0, 0), (1, 0), (2, 0)]]
    J = [[(-2, 0), (-1, 0), (0, 0), (0, -1)],
         [(-1, 0), (0, 0), (0, 1), (0, 2)],
         [(0, 1), (0, 0), (1, 0), (2, 0)],
         [(0, -2), (0, -1), (0, 0), (1, 0)]]
    L = [[(-2, 0), (-1, 0), (0, 0), (0, 1)],
         [(1, 0), (0, 0), (0, 1), (0, 2)],
         [(0, -1), (0, 0), (1, 0), (2, 0)],
         [(0, -2), (0, -1), (0, 0), (-1, 0)]]
    O = [[(0, 0), (0, 1), (1, 0), (1, 1)]]
    S = [[(-1, 0), (0, 0), (0, 1), (1, 1)],
         [(1, -1), (1, 0), (0, 0), (0, 1)]]
    T = [[(0, -1), (0, 0), (0, 1), (-1, 0)],
         [(-1, 0), (0, 0), (1, 0), (0, 1)],
         [(0, -1), (0, 0), (0, 1), (1, 0)],
         [(-1, 0), (0, 0), (1, 0), (0, -1)]]
    Z = [[(0, -1), (0, 0), (1, 0), (1, 1)],
         [(-1, 0), (0, 0), (0, -1), (1, -1)]]
    SHAPES_WITH_DIR = {
        'I': I, 'J': J, 'L': L, 'O': O, 'S': S, 'T': T, 'Z': Z
    }

    def __init__(self):
        self.shape = self.SHAPES[random.randint(0, len(self.SHAPES) - 1)]
        # 骨牌所在的行列
        self.center = (2, GRID_NUM_WIDTH // 2)
        self.dir = random.randint(0, len(self.SHAPES_WITH_DIR[self.shape]) - 1)
        self.color = CUBE_COLORS[random.randint(0, len(CUBE_COLORS) - 1)]

    def copy(self):
        """创建当前方块的副本"""
        new_cube = CubeShape()
        new_cube.shape = self.shape
        new_cube.center = self.center
        new_cube.dir = self.dir
        new_cube.color = self.color
        return new_cube

    def get_all_gridpos(self, center=None):
        curr_shape = self.SHAPES_WITH_DIR[self.shape][self.dir]
        if center is None:
            center = [self.center[0], self.center[1]]

        return [(cube[0] + center[0], cube[1] + center[1])
                for cube in curr_shape]

    def conflict(self, center):
        for cube in self.get_all_gridpos(center):
            # 超出屏幕之外，说明不合法
            if cube[0] < 0 or cube[1] < 0 or cube[0] >= GRID_NUM_HEIGHT or \
                    cube[1] >= GRID_NUM_WIDTH:
                return True

            # 不为None，说明之前已经有小方块存在了，也不合法
            if screen_color_matrix[cube[0]][cube[1]] is not None:
                return True

        return False

    def rotate(self):
        new_dir = self.dir + 1
        new_dir %= len(self.SHAPES_WITH_DIR[self.shape])
        old_dir = self.dir
        self.dir = new_dir
        if self.conflict(self.center):
            self.dir = old_dir
            return False
        return True

    def down(self):
        center = (self.center[0] + 1, self.center[1])
        if self.conflict(center):
            return False
        self.center = center
        return True

    def left(self):
        center = (self.center[0], self.center[1] - 1)
        if self.conflict(center):
            return False
        self.center = center
        return True

    def right(self):
        center = (self.center[0], self.center[1] + 1)
        if self.conflict(center):
            return False
        self.center = center
        return True

    def hard_drop(self):
        """硬降落：直接落到底部"""
        while self.down():
            pass
        return True

    def draw(self):
        for cube in self.get_all_gridpos():
            pygame.draw.rect(screen, self.color,
                             (cube[1] * GRID_WIDTH, cube[0] * GRID_WIDTH,
                              GRID_WIDTH, GRID_WIDTH))
            pygame.draw.rect(screen, WHITE,
                             (cube[1] * GRID_WIDTH, cube[0] * GRID_WIDTH,
                              GRID_WIDTH, GRID_WIDTH),
                             1)

    def draw_ghost(self):
        """绘制幽灵方块（显示最佳落点）"""
        ghost_cube = self.copy()
        ghost_cube.hard_drop()
        
        # 绘制半透明的幽灵方块
        for cube in ghost_cube.get_all_gridpos():
            # 创建半透明的颜色
            ghost_color = list(self.color)
            if len(ghost_color) == 3:
                ghost_color = ghost_color + [128]  # 添加透明度
            elif len(ghost_color) == 4:
                ghost_color[3] = 128
            
            # 绘制幽灵方块
            s = pygame.Surface((GRID_WIDTH, GRID_WIDTH), pygame.SRCALPHA)
            s.fill(tuple(ghost_color))
            screen.blit(s, (cube[1] * GRID_WIDTH, cube[0] * GRID_WIDTH))
            
            # 绘制边框
            pygame.draw.rect(screen, WHITE,
                            (cube[1] * GRID_WIDTH, cube[0] * GRID_WIDTH,
                             GRID_WIDTH, GRID_WIDTH),
                            1, 2)  # 2像素的虚线边框


class TetrisAI:
    """俄罗斯方块AI"""
    
    def __init__(self):
        pass
    
    def evaluate_position(self, matrix):
        """评估当前位置的分数"""
        score = 0
        
        # 1. 计算高度（越低越好）
        max_height = 0
        for col in range(GRID_NUM_WIDTH):
            height = 0
            for row in range(GRID_NUM_HEIGHT):
                if matrix[row][col] is not None:
                    height = GRID_NUM_HEIGHT - row
                    break
            max_height = max(max_height, height)
        score -= max_height * 10
        
        # 2. 计算完整行数（越多越好）
        complete_lines = 0
        liveScores = [0, 0, 0, 500, 18000] if max_height < 12 else [0,2000,2000,3000,5000]
        for row in range(GRID_NUM_HEIGHT):
            if all(matrix[row][col] is not None for col in range(GRID_NUM_WIDTH)):
                complete_lines += 1
        # score += complete_lines * 1000
        score += liveScores[complete_lines]
        
        # 3. 计算空洞数量（越少越好）
        holes = 0
        for col in range(GRID_NUM_WIDTH):
            found_block = False
            for row in range(GRID_NUM_HEIGHT):
                if matrix[row][col] is not None:
                    found_block = True
                elif found_block and matrix[row][col] is None:
                    holes += 1
        score -= holes * 50
        
        # 4. 计算凹凸不平度（越平滑越好）
        heights = []
        for col in range(GRID_NUM_WIDTH):
            for row in range(GRID_NUM_HEIGHT):
                if matrix[row][col] is not None:
                    heights.append(GRID_NUM_HEIGHT - row)
                    break
            else:
                heights.append(0)
        
        bumpiness = 0
        maxHeightDiff = 0  # 沟槽预留
        for i in range(len(heights) - 1):
            maxHeightDiff = max(maxHeightDiff, abs(heights[i] - heights[i + 1]))
            bumpiness += abs(heights[i] - heights[i + 1])
        score -= (bumpiness - maxHeightDiff) * 5
        
        # 5. 检查是否会制造井（避免在两侧都有方块的地方制造深井）
        wells = 0
        for col in range(1, GRID_NUM_WIDTH - 1):
            left_height = 0
            right_height = 0
            for row in range(GRID_NUM_HEIGHT):
                if matrix[row][col-1] is not None:
                    left_height = GRID_NUM_HEIGHT - row
                    break
            for row in range(GRID_NUM_HEIGHT):
                if matrix[row][col+1] is not None:
                    right_height = GRID_NUM_HEIGHT - row
                    break
            
            if left_height > 0 and right_height > 0:
                current_height = 0
                for row in range(GRID_NUM_HEIGHT):
                    if matrix[row][col] is not None:
                        current_height = GRID_NUM_HEIGHT - row
                        break
                if current_height < min(left_height, right_height) - 2:
                    wells += (min(left_height, right_height) - current_height)
        
        score -= 0 if max_height < 10 else wells * 30
        
        return score
    
    def simulate_drop(self, cube_shape, target_dir, target_x):
        """模拟方块放置到指定位置"""
        # 创建方块的副本
        test_cube = cube_shape.copy()

        # 旋转到目标方向
        test_cube.dir = target_dir
        
        # 移动到目标水平位置
        while test_cube.center[1] < target_x:
            if not test_cube.right():
                return []
        while test_cube.center[1] > target_x:
            if not test_cube.left():
                return []

        # 硬降落到底部
        test_cube.hard_drop()

        # 检查是否合法
        if test_cube.conflict(test_cube.center):
            return None

        # 创建新的矩阵来模拟放置
        new_matrix = copy.deepcopy(screen_color_matrix)
        # 放置方块到矩阵
        for cube in test_cube.get_all_gridpos():
            if 0 <= cube[0] < GRID_NUM_HEIGHT and 0 <= cube[1] < GRID_NUM_WIDTH:
                new_matrix[cube[0]][cube[1]] = test_cube.color
        
        return new_matrix
    
    def find_best_move(self, cube_shape):
        """寻找最佳移动"""
        best_score = -float('inf')
        best_move = None
        best_path = []
        # 获取当前方块的所有可能旋转
        shape_info = CubeShape.SHAPES_WITH_DIR[cube_shape.shape]
        num_rotations = len(shape_info)

        # 遍历所有可能的旋转
        for rotation in range(num_rotations):
            # 创建测试方块并旋转
            test_cube = cube_shape.copy()
            test_cube.dir = rotation
            # 获取方块的宽度
            shape_cells = shape_info[rotation]
            min_x = min(cell[1] for cell in shape_cells)
            max_x = max(cell[1] for cell in shape_cells)
            shape_width = max_x - min_x + 1

            # 遍历所有可能的水平位置
            for x in range(-min_x, GRID_NUM_WIDTH - max_x):
                # 模拟放置
                result_matrix = self.simulate_drop(cube_shape, rotation, x)

                if result_matrix is not None:
                    # 评估这个位置
                    score = self.evaluate_position(result_matrix)

                    # 添加额外奖励：靠近中间位置
                    center_x = GRID_NUM_WIDTH // 2
                    distance_from_center = abs(x + shape_width // 2 - center_x)
                    score -= distance_from_center * 2
                    if score > best_score:

                        best_score = score
                        best_move = (rotation, x)
                        
                        # 计算移动路径
                        path = self.calculate_move_path(cube_shape, rotation, x)
                        best_path = path
        return best_move, best_path
    
    def calculate_move_path(self, cube_shape, target_rotation, target_x):
        """计算从当前位置到目标位置的移动路径"""
        path = []
        current_cube = cube_shape.copy()
        
        # 计算需要的旋转次数
        rotations_needed = (target_rotation - current_cube.dir) % len(
            CubeShape.SHAPES_WITH_DIR[current_cube.shape]
        )
        
        # 添加旋转操作
        for _ in range(rotations_needed):
            path.append('rotate')
        
        # 计算水平移动
        move_x = target_x - current_cube.center[1]
        if move_x > 0:
            for _ in range(move_x):
                path.append('right')
        elif move_x < 0:
            for _ in range(-move_x):
                path.append('left')
        
        # 最后添加硬降落
        path.append('hard_drop')
        
        return path
    
    def execute_move_path(self, cube_shape, path):
        """执行移动路径中的下一步"""
        if not path:
            return False, False
        
        move = path.pop(0)
        isOK = True
        if move == 'rotate':
            isOK = cube_shape.rotate()
        elif move == 'left':
            isOK = cube_shape.left()
        elif move == 'right':
            isOK = cube_shape.right()
        elif move == 'hard_drop':
            cube_shape.hard_drop()
            return True, isOK  # 硬降落完成后，方块放置完成
        
        return False, isOK


def draw_grids():
    for i in range(GRID_NUM_WIDTH):
        pygame.draw.line(screen, LINE_COLOR,
                         (i * GRID_WIDTH, 0), (i * GRID_WIDTH, HEIGHT))

    for i in range(GRID_NUM_HEIGHT):
        pygame.draw.line(screen, LINE_COLOR,
                         (0, i * GRID_WIDTH), (WIDTH, i * GRID_WIDTH))

    pygame.draw.line(screen, WHITE,
                     (GRID_WIDTH * GRID_NUM_WIDTH, 0),
                     (GRID_WIDTH * GRID_NUM_WIDTH, GRID_WIDTH * GRID_NUM_HEIGHT))


def draw_matrix():
    for i, row in zip(range(GRID_NUM_HEIGHT), screen_color_matrix):
        for j, color in zip(range(GRID_NUM_WIDTH), row):
            if color is not None:
                pygame.draw.rect(screen, color,
                                 (j * GRID_WIDTH, i * GRID_WIDTH,
                                  GRID_WIDTH, GRID_WIDTH))
                pygame.draw.rect(screen, WHITE,
                                 (j * GRID_WIDTH, i * GRID_WIDTH,
                                  GRID_WIDTH, GRID_WIDTH), 2)


def draw_score():
    show_text(screen, u'得分：{}'.format(score), 20, WIDTH + SIDE_WIDTH // 2, 100)
    show_text(screen, u'等级：{}'.format(level), 20, WIDTH + SIDE_WIDTH // 2, 150)
    show_text(screen, u'{}'.format(lineCount), 20, WIDTH + SIDE_WIDTH // 2, 50)
    
    # 显示自动模式状态
    mode_color = GREEN if auto_mode else RED
    mode_text = "自动模式" if auto_mode else "手动模式"
    show_text(screen, u'模式：{}'.format(mode_text), 20, 
              WIDTH + SIDE_WIDTH // 2, 200, mode_color)
    
    # 显示操作说明
    show_text(screen, u'操作说明：', 18, WIDTH + SIDE_WIDTH // 2, 250)
    show_text(screen, u'← → : 左右移动', 16, WIDTH + SIDE_WIDTH // 2, 280)
    show_text(screen, u'↑ : 旋转', 16, WIDTH + SIDE_WIDTH // 2, 305)
    show_text(screen, u'↓ : 加速下落', 16, WIDTH + SIDE_WIDTH // 2, 330)
    show_text(screen, u'空格 : 硬降落', 16, WIDTH + SIDE_WIDTH // 2, 355)
    show_text(screen, u'A : 切换自动模式', 16, WIDTH + SIDE_WIDTH // 2, 380)
    show_text(screen, u'ESC : 退出', 16, WIDTH + SIDE_WIDTH // 2, 405)


def remove_full_line():
    global screen_color_matrix
    global score
    global level
    global lineCount
    bonus_score = [0,1,3,6,10]
    new_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
    index = GRID_NUM_HEIGHT - 1
    n_full_line = 0
    for i in range(GRID_NUM_HEIGHT - 1, -1, -1):
        is_full = True
        for j in range(GRID_NUM_WIDTH):
            if screen_color_matrix[i][j] is None:
                is_full = False
                continue
        if not is_full:
            new_matrix[index] = screen_color_matrix[i]
            index -= 1
        else:
            n_full_line += 1
    score += bonus_score[n_full_line]
    level = score // 20 + 1 if level < 30 else 30
    screen_color_matrix = new_matrix
    if n_full_line > 0:
        lineCount[n_full_line-1] += 1

def show_welcome(screen):
    show_text(screen, u'俄罗斯方块-自动模式', 30, WIDTH / 2, HEIGHT / 2 - 50)
    show_text(screen, u'按任意键开始游戏', 20, WIDTH / 2, HEIGHT / 2)
    show_text(screen, u'按A键切换自动模式', 20, WIDTH / 2, HEIGHT / 2 + 40)


# 创建AI实例
ai = TetrisAI()

running = True
gameover = True
counter = 0
live_cube = None
move_counter = 0
while running:
    clock.tick(FPS)
    
    # 自动模式控制
    if auto_mode and live_cube is not None and not gameover:
        auto_move_counter += 2
        if auto_move_counter >= auto_move_interval:
            auto_move_counter = 0

            
            # 如果还没有计算最佳移动，先计算
            if not best_move_path:
                best_move, best_move_path = ai.find_best_move(live_cube)
            
                
            # 执行移动路径中的下一步
            if best_move_path:
                move_completed, isOK = ai.execute_move_path(live_cube, best_move_path)
                
                if not isOK:
                    gameover = True
                    live_cube = None
                    score = 0
                    screen_color_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]

                elif move_completed:
                    # 方块放置完成，重置路径
                    best_move_path = []
                    
                    # 将方块添加到矩阵
                    for cube in live_cube.get_all_gridpos():
                        screen_color_matrix[cube[0]][cube[1]] = live_cube.color
                    
                    # 创建新方块
                    live_cube = CubeShape()
                    
                    # 检查游戏是否结束
                    if live_cube.conflict(live_cube.center):
                        gameover = True
                        live_cube = None
                        score = 0
                        screen_color_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
                    
                    # 消除满行
                    remove_full_line()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if gameover:
                gameover = False
                live_cube = CubeShape()
                auto_mode = False  # 游戏重新开始时默认手动模式
                best_move_path = []  # 重置路径
                score = 0
                break
            
            if event.key == pygame.K_a:  # A键切换自动模式
                auto_mode = not auto_mode
                best_move_path = []  # 切换模式时重置路径
                auto_move_counter = 0
            
            if not auto_mode:  # 手动模式下的控制
                if live_cube is not None:
                    if event.key == pygame.K_LEFT:
                        live_cube.left()
                        counter -= 1
                    elif event.key == pygame.K_RIGHT:
                        live_cube.right()
                        counter -= 1
                    elif event.key == pygame.K_DOWN:
                        live_cube.down()
                    elif event.key == pygame.K_UP:
                        live_cube.rotate()
                        counter -= 1
                    elif event.key == pygame.K_SPACE:
                        live_cube.hard_drop()
                        # 方块放置到矩阵
                        for cube in live_cube.get_all_gridpos():
                            screen_color_matrix[cube[0]][cube[1]] = live_cube.color
                        
                        # 创建新方块
                        live_cube = CubeShape()
                        
                        # 检查游戏是否结束
                        if live_cube.conflict(live_cube.center):
                            gameover = True
                            score = 0
                            live_cube = None
                            screen_color_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
                        
                        # 消除满行
                        remove_full_line()

    # 手动模式下的自动下落
    if gameover is False and counter % (FPS // level) == 0 and not auto_mode:
        if live_cube.down() == False:
            for cube in live_cube.get_all_gridpos():
                screen_color_matrix[cube[0]][cube[1]] = live_cube.color
            live_cube = CubeShape()
            if live_cube.conflict(live_cube.center):
                gameover = True
                live_cube = None
                score = 0
                screen_color_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
        remove_full_line()
    
    counter += 1
    
    # 绘制游戏界面
    screen.fill(BLACK)
    draw_grids()
    draw_matrix()
    draw_score()
    
    if live_cube is not None:
        # 绘制幽灵方块（显示最佳落点）
        if auto_mode and best_move_path:
            live_cube.draw_ghost()
        live_cube.draw()
    
    if gameover:
        show_welcome(screen)
    
    pygame.display.update()

pygame.quit()
