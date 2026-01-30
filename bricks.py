# 打砖块游戏 - 美化版UI
import pygame
import sys
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)
RED = (220, 20, 60)
GREEN = (50, 205, 50)
YELLOW = (255, 215, 0)
ORANGE = (255, 165, 0)
PURPLE = (147, 112, 219)
CYAN = (0, 206, 209)
DARK_BLUE = (0, 0, 139)
BACKGROUND = (25, 25, 50)
# 降低UI面板透明度
UI_BACKGROUND = (40, 40, 70, 150)  # 从200降低到150
BUTTON_NORMAL = (70, 130, 180)
BUTTON_HOVER = (100, 149, 237)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("打砖块游戏")
clock = pygame.time.Clock()

# 初始化字体
try:
    font_title = pygame.font.SysFont("simhei", 48)
    font_large = pygame.font.SysFont("simhei", 36)
    font_medium = pygame.font.SysFont("simhei", 28)
    font_small = pygame.font.SysFont("simhei", 24)
    font_tiny = pygame.font.SysFont("simhei", 20)
except:
    font_title = pygame.font.Font(None, 48)
    font_large = pygame.font.Font(None, 36)
    font_medium = pygame.font.Font(None, 28)
    font_small = pygame.font.Font(None, 24)
    font_tiny = pygame.font.Font(None, 20)

# 缓存透明背景Surface
ui_panel_surface = None
instruction_panel_surface = None


def draw_rounded_rect(surface, rect, color, corner_radius):
    """绘制圆角矩形"""
    if corner_radius < 0:
        raise ValueError("Corner radius must be non-negative")
    if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
        raise ValueError(f"Corner radius {corner_radius} too large for the rect")

    # 绘制中间的矩形
    pygame.draw.rect(surface, color, (rect.left, rect.top + corner_radius, rect.width, rect.height - 2 * corner_radius))
    pygame.draw.rect(surface, color, (rect.left + corner_radius, rect.top, rect.width - 2 * corner_radius, rect.height))

    # 绘制四个圆角
    pygame.draw.circle(surface, color, (rect.left + corner_radius, rect.top + corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (rect.right - corner_radius, rect.top + corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (rect.left + corner_radius, rect.bottom - corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (rect.right - corner_radius, rect.bottom - corner_radius), corner_radius)


def draw_button(surface, rect, text, font, bg_color, text_color, hover_color=None, border_color=WHITE):
    """绘制美化按钮"""
    mouse_pos = pygame.mouse.get_pos()
    is_hover = rect.collidepoint(mouse_pos)

    if is_hover and hover_color:
        bg_color = hover_color

    # 绘制按钮背景
    draw_rounded_rect(surface, rect, bg_color, 10)

    # 绘制按钮边框
    pygame.draw.rect(surface, border_color, rect, 2, border_radius=10)

    # 绘制按钮文字
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

    return is_hover


def generate_staggered_bricks(brick_rows, brick_cols, brick_width, brick_height, brick_gap):
    """生成交错排列的砖块（类似砌砖效果）"""
    bricks = []
    brick_colors = [RED, ORANGE, YELLOW, GREEN, CYAN, PURPLE]

    # 计算起始位置，使砖块居中显示
    total_width = brick_cols * brick_width + (brick_cols - 1) * brick_gap
    start_x = (SCREEN_WIDTH - total_width) // 2
    start_y = 50  # 距离顶部的距离

    for row in range(brick_rows):
        # 交错排列：偶数行正常，奇数行偏移半个砖块
        offset_x = (brick_width + brick_gap) // 2 if row % 2 == 1 else 0

        for col in range(brick_cols):
            brick_x = start_x + col * (brick_width + brick_gap) + offset_x
            brick_y = start_y + row * (brick_height + brick_gap)

            # 确保砖块不超出屏幕边界
            if brick_x + brick_width <= SCREEN_WIDTH and brick_x >= 0:
                brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
                # 为不同行分配不同颜色
                color = brick_colors[row % len(brick_colors)]
                bricks.append((brick, color))

    return bricks


def draw_game_ui(surface, lives, score, brick_count):
    """绘制游戏UI界面"""
    global ui_panel_surface
    # 绘制UI背景面板
    ui_panel = pygame.Rect(10, 10, 200, 100)
    if ui_panel_surface is None or ui_panel_surface.get_size() != (ui_panel.width, ui_panel.height):
        ui_panel_surface = pygame.Surface((ui_panel.width, ui_panel.height), pygame.SRCALPHA)
        ui_panel_surface.fill(UI_BACKGROUND)
    surface.blit(ui_panel_surface, (ui_panel.x, ui_panel.y))
    pygame.draw.rect(surface, (100, 100, 200), ui_panel, 2, border_radius=10)

    # 绘制生命数
    lives_text = font_small.render(f"生命: {lives}", True, WHITE)
    surface.blit(lives_text, (20, 20))

    # 绘制分数
    score_text = font_small.render(f"分数: {score}", True, WHITE)
    surface.blit(score_text, (20, 50))

    # 绘制砖块数量
    bricks_text = font_small.render(f"剩余砖块: {brick_count}", True, WHITE)
    surface.blit(bricks_text, (20, 80))

    # 绘制游戏标题
    title_text = font_title.render("打砖块", True, YELLOW)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 25))
    surface.blit(title_text, title_rect)


def draw_game_over(surface, won, score):
    """绘制游戏结束界面"""
    # 半透明覆盖层 (稍微降低透明度)
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # 从180降低到150
    surface.blit(overlay, (0, 0))

    # 游戏结束标题
    if won:
        game_over_text = font_title.render("恭喜通关!", True, GREEN)
    else:
        game_over_text = font_title.render("游戏结束!", True, RED)

    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
    surface.blit(game_over_text, game_over_rect)

    # 显示最终分数
    score_text = font_large.render(f"最终分数: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
    surface.blit(score_text, score_rect)

    # 绘制按钮
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 30, 200, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)

    restart_hover = draw_button(surface, restart_button, "重新开始", font_medium,
                               BUTTON_NORMAL, WHITE, BUTTON_HOVER)
    quit_hover = draw_button(surface, quit_button, "退出游戏", font_medium,
                            BUTTON_NORMAL, WHITE, BUTTON_HOVER)

    return restart_button, quit_button


def draw_instructions(surface, show_instructions):
    """绘制游戏说明"""
    global instruction_panel_surface
    # 只在需要显示时绘制操作说明
    if show_instructions:
        # 绘制说明面板
        panel_rect = pygame.Rect(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 150, 210, 140)
        if instruction_panel_surface is None or instruction_panel_surface.get_size() != (panel_rect.width, panel_rect.height):
            instruction_panel_surface = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
            instruction_panel_surface.fill(UI_BACKGROUND)
        surface.blit(instruction_panel_surface, (panel_rect.x, panel_rect.y))
        pygame.draw.rect(surface, (100, 100, 200), panel_rect, 2, border_radius=10)

        # 绘制说明文字
        title = font_tiny.render("操作说明", True, YELLOW)
        surface.blit(title, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 140))

        instructions = [
            "← → : 移动挡板",
            "空格: 重新开始",
            "ESC : 退出游戏"
        ]

        for i, line in enumerate(instructions):
            text = font_tiny.render(line, True, WHITE)
            surface.blit(text, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 110 + i * 25))


# 预渲染星空背景
star_positions = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(50)]
star_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
for x, y in star_positions:
    pygame.draw.circle(star_surface, (100, 100, 150), (x, y), 1)


def game_loop():
    # 挡板和小球初始化
    paddle = pygame.Rect(SCREEN_WIDTH//2-60, SCREEN_HEIGHT-40, 120, 20)
    paddle_speed = 8
    ball = pygame.Rect(SCREEN_WIDTH//2-7, SCREEN_HEIGHT-60, 15, 15)
    ball_speed_x = 5
    ball_speed_y = -5

    # 游戏状态
    game_over = False
    game_won = False
    lives = 3  # 生命数
    score = 0  # 分数
    # 操作说明显示控制
    show_instructions = True
    instruction_timer = 0
    INSTRUCTION_DURATION = 2000  # 2秒后隐藏操作说明

    # 生成交错砖块
    brick_rows = 6    # 砖块行数
    brick_cols = 10   # 砖块列数
    brick_width = 70  # 砖块宽度
    brick_height = 30 # 砖块高度
    brick_gap = 5     # 砖块间距

    # 生成交错排列的砖块
    bricks = generate_staggered_bricks(brick_rows, brick_cols, brick_width, brick_height, brick_gap)

    running = True
    while running:
        delta_time = clock.tick(60)

        # 更新操作说明计时器
        if show_instructions:
            instruction_timer += delta_time
            if instruction_timer >= INSTRUCTION_DURATION:
                show_instructions = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # 按空格键重新开始游戏
                if (game_over or game_won) and event.key == pygame.K_SPACE:
                    return True  # 返回True表示重新开始
                # 按ESC键退出
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # 处理按钮点击事件
                mouse_pos = event.pos
                if game_over or game_won:
                    if restart_button.collidepoint(mouse_pos):
                        return True  # 重新开始
                    elif quit_button.collidepoint(mouse_pos):
                        running = False

        if not game_over and not game_won:
            # 挡板控制
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and paddle.left > 0:
                paddle.x -= paddle_speed
            if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
                paddle.x += paddle_speed

            # 小球移动
            ball.x += ball_speed_x
            ball.y += ball_speed_y

            # 小球边界反弹
            if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
                ball_speed_x *= -1
            if ball.top <= 0:
                ball_speed_y *= -1

            # 小球碰到挡板反弹
            if ball.colliderect(paddle):
                ball_speed_y *= -1
                # 优化：让小球反弹方向随挡板位置变化（更真实）
                ball_speed_x = (ball.centerx - paddle.centerx) / 3  # 左右偏移影响x速度

            # 小球碰到底部 → 减少生命数
            if ball.bottom >= SCREEN_HEIGHT:
                lives -= 1
                if lives <= 0:
                    game_over = True  # 生命用完，游戏结束
                else:
                    # 重置小球位置和速度
                    ball.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT-60)
                    ball_speed_x = 5
                    ball_speed_y = -5

            # 小球碰到砖块 → 砖块消失+小球反弹+增加分数
            for brick, color in bricks[:]:  # 切片遍历（避免删除时索引异常）
                if ball.colliderect(brick):
                    bricks.remove((brick, color))  # 删除被碰到的砖块
                    ball_speed_y *= -1     # 小球y方向反弹
                    score += 10  # 增加分数
                    break  # 避免一次碰到多个砖块

            # 检查是否所有砖块都被消除
            if len(bricks) == 0:
                game_won = True

        # 绘制部分
        screen.fill(BACKGROUND)

        # 绘制星空背景效果
        screen.blit(star_surface, (0, 0))

        # 绘制挡板和小球
        pygame.draw.rect(screen, BLUE, paddle, border_radius=5)
        pygame.draw.ellipse(screen, RED, ball)

        # 绘制所有砖块
        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick, border_radius=3)
            # 绘制砖块边框
            pygame.draw.rect(screen, WHITE, brick, 1, border_radius=3)

        # 绘制UI信息
        draw_game_ui(screen, lives, score, len(bricks))

        # 绘制操作说明（2秒后自动消失）
        draw_instructions(screen, show_instructions)

        # 游戏结束提示
        if game_over or game_won:
            restart_button, quit_button = draw_game_over(screen, game_won, score)

        pygame.display.flip()

    return False  # 返回False表示退出游戏


def main():
    while True:
        restart = game_loop()
        if not restart:
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

