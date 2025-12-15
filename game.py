# -*- coding: utf-8 -*-
"""
游戏核心逻辑模块
包含游戏的所有核心类和函数
"""

import pygame
import random
import math
import time
import json
from datetime import datetime
from config import *


class Particle_xzh:
    """粒子效果类 - 用于砖块破碎特效"""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1)
        self.color = color
        self.life = 30  # 生命周期
        self.size = random.randint(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3  # 重力效果
        self.life -= 1
        self.size = max(1, self.size - 0.1)

    def draw(self, screen):
        alpha = int(255 * (self.life / 30))
        color = (*self.color, alpha) if len(self.color) == 3 else self.color
        try:
            s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (self.size, self.size), int(self.size))
            screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))
        except:
            pygame.draw.circle(screen, self.color[:3], (int(self.x), int(self.y)), int(self.size))

    def is_dead(self):
        return self.life <= 0


class Paddle_xzh:
    """挡板类"""

    def __init__(self, x, y, width):
        """
        初始化挡板
        :param x: X坐标
        :param y: Y坐标
        :param width: 挡板宽度
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = PADDLE_HEIGHT_XZH
        self.speed = PADDLE_SPEED_XZH
        self.color = PADDLE_COLOR_XZH

    def move_left_xzh(self):
        """向左移动挡板"""
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def move_right_xzh(self):
        """向右移动挡板"""
        self.x += self.speed
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width

    def draw_xzh(self, screen):
        """
        绘制挡板 - 带渐变和发光效果
        :param screen: Pygame屏幕对象
        """
        # 绘制发光效果（外围）
        glow_surf = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*COLOR_CYAN_XZH, 30), (0, 0, self.width + 10, self.height + 10), border_radius=8)
        screen.blit(glow_surf, (self.x - 5, self.y - 5))

        # 绘制主体渐变效果
        for i in range(self.height):
            ratio = i / self.height
            r = int(COLOR_BLUE_XZH[0] + (100 - COLOR_BLUE_XZH[0]) * ratio)
            g = int(COLOR_BLUE_XZH[1] + (150 - COLOR_BLUE_XZH[1]) * ratio)
            b = int(COLOR_BLUE_XZH[2] + (255 - COLOR_BLUE_XZH[2]) * ratio)
            pygame.draw.rect(screen, (r, g, b), (self.x, self.y + i, self.width, 1))

        # 绘制高光
        highlight_surf = pygame.Surface((self.width, self.height // 3), pygame.SRCALPHA)
        pygame.draw.rect(highlight_surf, (255, 255, 255, 80), (0, 0, self.width, self.height // 3), border_radius=5)
        screen.blit(highlight_surf, (self.x, self.y + 2))

        # 绘制边框
        pygame.draw.rect(screen, (100, 200, 255), (self.x, self.y, self.width, self.height), 2, border_radius=5)

    def get_rect_xzh(self):
        """
        获取挡板的矩形区域
        :return: pygame.Rect对象
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def adjust_width_xzh(self, delta):
        """
        调整挡板宽度
        :param delta: 宽度变化量
        """
        self.width += delta
        if self.width < PADDLE_WIDTH_MIN_XZH:
            self.width = PADDLE_WIDTH_MIN_XZH
        elif self.width > PADDLE_WIDTH_MAX_XZH:
            self.width = PADDLE_WIDTH_MAX_XZH

    def adjust_speed_xzh(self, delta):
        """
        调整挡板速度
        :param delta: 速度变化量
        """
        self.speed += delta
        if self.speed > PADDLE_SPEED_MAX_XZH:
            self.speed = PADDLE_SPEED_MAX_XZH


class Ball_xzh:
    """球类"""

    def __init__(self, x, y, speed):
        """
        初始化球
        :param x: X坐标
        :param y: Y坐标
        :param speed: 球速
        """
        self.x = x
        self.y = y
        self.radius = BALL_RADIUS_XZH
        self.speed = speed
        self.dx = 0
        self.dy = 0
        self.active = False
        self.color = BALL_COLOR_XZH

    def launch_xzh(self):
        """发射球"""
        if not self.active:
            angle = random.uniform(-60, 60)  # 随机角度（度）
            angle_rad = math.radians(angle)
            self.dx = self.speed * math.sin(angle_rad)
            self.dy = -self.speed * math.cos(angle_rad)
            self.active = True

    def move_xzh(self):
        """移动球"""
        if self.active:
            self.x += self.dx
            self.y += self.dy

    def bounce_wall_xzh(self):
        """处理球与墙壁的碰撞"""
        # 左右墙壁
        if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
            self.dx = -self.dx
            # 修正位置防止穿墙
            if self.x - self.radius < 0:
                self.x = self.radius
            if self.x + self.radius > SCREEN_WIDTH:
                self.x = SCREEN_WIDTH - self.radius

        # 顶部墙壁
        if self.y - self.radius <= 0:
            self.dy = -self.dy
            self.y = self.radius

    def bounce_paddle_xzh(self, paddle):
        """
        处理球与挡板的碰撞
        :param paddle: Paddle_xzh对象
        :return: 是否发生碰撞
        """
        if not self.active:
            return False

        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                               self.radius * 2, self.radius * 2)
        paddle_rect = paddle.get_rect_xzh()

        if ball_rect.colliderect(paddle_rect) and self.dy > 0:
            # 计算球击中挡板的相对位置
            hit_pos = (self.x - paddle.x) / paddle.width  # 0到1之间
            # 根据击中位置调整反弹角度
            angle = (hit_pos - 0.5) * 120  # -60到60度
            angle_rad = math.radians(angle)

            speed = math.sqrt(self.dx ** 2 + self.dy ** 2)
            self.dx = speed * math.sin(angle_rad)
            self.dy = -speed * math.cos(angle_rad)

            # 修正位置防止粘连
            self.y = paddle.y - self.radius
            return True
        return False

    def check_miss_xzh(self):
        """
        检查球是否掉落
        :return: 是否掉落
        """
        return self.y - self.radius > SCREEN_HEIGHT

    def reset_xzh(self, paddle):
        """
        重置球的位置
        :param paddle: Paddle_xzh对象
        """
        self.x = paddle.x + paddle.width / 2
        self.y = paddle.y - self.radius - 5
        self.dx = 0
        self.dy = 0
        self.active = False

    def draw_xzh(self, screen):
        """
        绘制球 - 带发光和渐变效果
        :param screen: Pygame屏幕对象
        """
        # 绘制发光效果（外围光晕）
        for i in range(3):
            glow_radius = self.radius + 6 - i * 2
            alpha = 40 - i * 10
            glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*COLOR_CYAN_XZH, alpha),
                             (glow_radius, glow_radius), glow_radius)
            screen.blit(glow_surf, (int(self.x - glow_radius), int(self.y - glow_radius)))

        # 绘制主球体（渐变效果）
        pygame.draw.circle(screen, (200, 200, 255), (int(self.x), int(self.y)), self.radius)

        # 绘制高光
        highlight_offset = self.radius // 3
        pygame.draw.circle(screen, (255, 255, 255),
                         (int(self.x - highlight_offset), int(self.y - highlight_offset)),
                         self.radius // 3)

        # 绘制边框
        pygame.draw.circle(screen, (150, 200, 255), (int(self.x), int(self.y)), self.radius, 2)

    def adjust_speed_xzh(self, delta):
        """
        调整球速
        :param delta: 速度变化量
        """
        current_speed = math.sqrt(self.dx ** 2 + self.dy ** 2)
        new_speed = current_speed + delta

        if new_speed < BALL_SPEED_MIN_XZH:
            new_speed = BALL_SPEED_MIN_XZH
        elif new_speed > BALL_SPEED_MAX_XZH:
            new_speed = BALL_SPEED_MAX_XZH

        if current_speed > 0:
            ratio = new_speed / current_speed
            self.dx *= ratio
            self.dy *= ratio

        self.speed = new_speed


class Brick_xzh:
    """砖块类"""

    def __init__(self, x, y, width, height, color, points):
        """
        初始化砖块
        :param x: X坐标
        :param y: Y坐标
        :param width: 宽度
        :param height: 高度
        :param color: 颜色
        :param points: 分数
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.points = points
        self.visible = True

    def draw_xzh(self, screen):
        """
        绘制砖块 - 带3D立体和光泽效果
        :param screen: Pygame屏幕对象
        """
        if self.visible:
            # 绘制阴影
            shadow_offset = 3
            shadow_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surf, (0, 0, 0, 50), (0, 0, self.width, self.height), border_radius=5)
            screen.blit(shadow_surf, (self.x + shadow_offset, self.y + shadow_offset))

            # 绘制渐变主体
            for i in range(self.height):
                ratio = i / self.height
                # 从亮到暗的渐变
                r = int(self.color[0] * (1 - ratio * 0.3))
                g = int(self.color[1] * (1 - ratio * 0.3))
                b = int(self.color[2] * (1 - ratio * 0.3))
                pygame.draw.rect(screen, (r, g, b), (self.x, self.y + i, self.width, 1))

            # 绘制高光（顶部）
            highlight_surf = pygame.Surface((self.width - 10, 8), pygame.SRCALPHA)
            pygame.draw.rect(highlight_surf, (255, 255, 255, 100), (0, 0, self.width - 10, 8), border_radius=3)
            screen.blit(highlight_surf, (self.x + 5, self.y + 3))

            # 绘制边框
            darker_color = tuple(max(0, c - 50) for c in self.color)
            pygame.draw.rect(screen, darker_color,
                           (self.x, self.y, self.width, self.height), 2, border_radius=5)

    def get_rect_xzh(self):
        """
        获取砖块的矩形区域
        :return: pygame.Rect对象
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Game_xzh:
    """游戏主类"""

    def __init__(self, mode=MODE_CLASSIC_XZH):
        """
        初始化游戏
        :param mode: 游戏模式
        """
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("智能自适应打砖块游戏")
            self.clock = pygame.time.Clock()

            # 使用系统中文字体
            try:
                # Windows 系统尝试使用微软雅黑
                self.font_large = pygame.font.SysFont('microsoftyahei', FONT_SIZE_LARGE_XZH)
                self.font_medium = pygame.font.SysFont('microsoftyahei', FONT_SIZE_MEDIUM_XZH)
                self.font_small = pygame.font.SysFont('microsoftyahei', FONT_SIZE_SMALL_XZH)
            except:
                # 如果微软雅黑不可用，尝试其他中文字体
                try:
                    self.font_large = pygame.font.SysFont('simhei', FONT_SIZE_LARGE_XZH)
                    self.font_medium = pygame.font.SysFont('simhei', FONT_SIZE_MEDIUM_XZH)
                    self.font_small = pygame.font.SysFont('simhei', FONT_SIZE_SMALL_XZH)
                except:
                    # 最后尝试使用默认字体
                    self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE_XZH)
                    self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM_XZH)
                    self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL_XZH)

            self.mode = mode
            self.running = True
            self.game_started = False
            self.game_over = False
            self.game_won = False

            # 游戏统计数据
            self.score = 0
            self.lives = INITIAL_LIVES_XZH if mode == MODE_CLASSIC_XZH else CHALLENGE_LIVES_XZH
            self.bricks_hit = 0
            self.bricks_missed = 0
            self.total_bricks_hit = 0  # 新增：累计击中砖块数（不重置）
            self.total_bricks_missed = 0  # 新增：累计未击中数（不重置）
            self.last_check_hit_count = 0  # 新增：上次检查时的击中数
            self.level = 1  # 新增：关卡数（用于挑战模式）
            self.particles = []  # 粒子效果列表
            self.start_time = None
            self.end_time = None

            # 初始化游戏对象
            self.init_game_objects_xzh()

        except Exception as e:
            print(f"游戏初始化错误: {e}")
            raise

    def init_game_objects_xzh(self):
        """初始化游戏对象"""
        # 根据模式设置初始速度
        initial_speed = BALL_SPEED_DEFAULT_XZH
        if self.mode == MODE_CHALLENGE_XZH:
            initial_speed *= CHALLENGE_SPEED_MULTIPLIER_XZH

        # 创建挡板
        paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH_DEFAULT_XZH) / 2
        paddle_y = SCREEN_HEIGHT - 50
        self.paddle = Paddle_xzh(paddle_x, paddle_y, PADDLE_WIDTH_DEFAULT_XZH)

        # 创建球
        ball_x = paddle_x + PADDLE_WIDTH_DEFAULT_XZH / 2
        ball_y = paddle_y - BALL_RADIUS_XZH - 5
        self.ball = Ball_xzh(ball_x, ball_y, initial_speed)

        # 创建砖块
        self.bricks = []
        rows = BRICK_ROWS_XZH if self.mode == MODE_CLASSIC_XZH else CHALLENGE_BRICK_ROWS_XZH
        for row in range(rows):
            for col in range(BRICK_COLS_XZH):
                brick_x = BRICK_OFFSET_LEFT_XZH + col * (BRICK_WIDTH_XZH + BRICK_PADDING_XZH)
                brick_y = BRICK_OFFSET_TOP_XZH + row * (BRICK_HEIGHT_XZH + BRICK_PADDING_XZH)
                color = BRICK_COLORS_XZH[row % len(BRICK_COLORS_XZH)]
                brick = Brick_xzh(brick_x, brick_y, BRICK_WIDTH_XZH,
                                BRICK_HEIGHT_XZH, color, POINTS_PER_BRICK_XZH)
                self.bricks.append(brick)

    def regenerate_bricks_xzh(self):
        """重新生成砖块（用于挑战模式的无尽模式）"""
        self.bricks = []
        rows = BRICK_ROWS_XZH if self.mode == MODE_CLASSIC_XZH else CHALLENGE_BRICK_ROWS_XZH
        for row in range(rows):
            for col in range(BRICK_COLS_XZH):
                brick_x = BRICK_OFFSET_LEFT_XZH + col * (BRICK_WIDTH_XZH + BRICK_PADDING_XZH)
                brick_y = BRICK_OFFSET_TOP_XZH + row * (BRICK_HEIGHT_XZH + BRICK_PADDING_XZH)
                color = BRICK_COLORS_XZH[row % len(BRICK_COLORS_XZH)]
                brick = Brick_xzh(brick_x, brick_y, BRICK_WIDTH_XZH,
                                BRICK_HEIGHT_XZH, color, POINTS_PER_BRICK_XZH)
                self.bricks.append(brick)

        # 关卡提升
        self.level += 1
        print(f"挑战模式 - 进入第 {self.level} 关!")

    def handle_events_xzh(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.ball.active:
                    if not self.game_started:
                        self.game_started = True
                        self.start_time = time.time()
                    self.ball.launch_xzh()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

        # 处理键盘持续按键
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.paddle.move_left_xzh()
            if not self.ball.active:
                self.ball.x = self.paddle.x + self.paddle.width / 2
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.paddle.move_right_xzh()
            if not self.ball.active:
                self.ball.x = self.paddle.x + self.paddle.width / 2

    def update_xzh(self):
        """更新游戏状态"""
        if not self.game_started or self.game_over or self.game_won:
            return

        # 移动球
        self.ball.move_xzh()

        # 球与墙壁碰撞
        self.ball.bounce_wall_xzh()

        # 球与挡板碰撞
        if self.ball.bounce_paddle_xzh(self.paddle):
            self.bricks_missed += 1  # 记录未击中砖块的次数
            self.total_bricks_missed += 1  # 累计未击中数

        # 球与砖块碰撞
        self.check_brick_collision_xzh()

        # 检查球是否掉落
        if self.ball.check_miss_xzh():
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
                self.end_time = time.time()
            else:
                self.ball.reset_xzh(self.paddle)

        # 检查是否获胜或重新生成砖块
        if all(not brick.visible for brick in self.bricks):
            if self.mode == MODE_CHALLENGE_XZH:
                # 挑战模式：重新生成砖块，继续游戏（无尽模式）
                self.regenerate_bricks_xzh()
                # 球回到挡板上方，但不重置为未发射状态
                if self.ball.active:
                    self.ball.reset_xzh(self.paddle)
                    self.ball.launch_xzh()  # 自动发射球
            else:
                # 经典模式：游戏胜利
                self.game_won = True
                self.end_time = time.time()

        # 智能难度调整
        self.adjust_difficulty_xzh()

        # 更新粒子效果
        for particle in self.particles[:]:
            particle.update()
            if particle.is_dead():
                self.particles.remove(particle)

    def check_brick_collision_xzh(self):
        """检查球与砖块的碰撞"""
        if not self.ball.active:
            return

        ball_rect = pygame.Rect(self.ball.x - self.ball.radius,
                               self.ball.y - self.ball.radius,
                               self.ball.radius * 2, self.ball.radius * 2)

        for brick in self.bricks:
            if brick.visible:
                brick_rect = brick.get_rect_xzh()
                if ball_rect.colliderect(brick_rect):
                    brick.visible = False
                    self.score += brick.points
                    self.bricks_hit += 1
                    self.total_bricks_hit += 1  # 累计击中数

                    # 生成粒子效果
                    brick_center_x = brick.x + brick.width / 2
                    brick_center_y = brick.y + brick.height / 2
                    for _ in range(15):  # 生成15个粒子
                        particle = Particle_xzh(brick_center_x, brick_center_y, brick.color)
                        self.particles.append(particle)

                    # 计算碰撞方向并反弹
                    self.calculate_bounce_xzh(brick_rect)
                    break

    def calculate_bounce_xzh(self, brick_rect):
        """
        计算球的反弹方向
        :param brick_rect: 砖块的矩形区域
        """
        # 计算球心到砖块各边的距离
        left_dist = abs(self.ball.x - brick_rect.left)
        right_dist = abs(self.ball.x - brick_rect.right)
        top_dist = abs(self.ball.y - brick_rect.top)
        bottom_dist = abs(self.ball.y - brick_rect.bottom)

        min_dist = min(left_dist, right_dist, top_dist, bottom_dist)

        # 根据最近的边确定反弹方向
        if min_dist in (left_dist, right_dist):
            self.ball.dx = -self.ball.dx
        else:
            self.ball.dy = -self.ball.dy

    def adjust_difficulty_xzh(self):
        """智能难度调整系统 - 渐进式难度提升"""
        # 检查是否达到检查间隔
        if self.total_bricks_hit - self.last_check_hit_count >= DIFFICULTY_CHECK_INTERVAL_XZH:
            # 计算当前阶段的命中率（使用短期统计）
            if self.bricks_hit > 0 or self.bricks_missed > 0:
                total_attempts = self.bricks_hit + self.bricks_missed
                hit_rate = self.bricks_hit / total_attempts if total_attempts > 0 else 0

                # 如果命中率高于阈值，增加难度
                if hit_rate > HIT_RATE_THRESHOLD_HIGH_XZH:
                    # 缩短挡板宽度
                    old_width = self.paddle.width
                    self.paddle.adjust_width_xzh(-PADDLE_WIDTH_ADJUSTMENT_XZH)

                    # 只有当挡板实际缩短时，才增加移动速度（防止达到最小宽度后速度持续增加）
                    if self.paddle.width < old_width:
                        self.paddle.adjust_speed_xzh(PADDLE_SPEED_ADJUSTMENT_XZH)
                        print(f"难度提升! 挡板宽度: {self.paddle.width:.0f}, 移动速度: {self.paddle.speed:.1f}")

            # 更新检查点和重置短期统计
            self.last_check_hit_count = self.total_bricks_hit
            self.bricks_hit = 0
            self.bricks_missed = 0

    def draw_xzh(self):
        """绘制游戏画面"""
        # 绘制渐变背景
        self.draw_background_xzh()

        # 绘制游戏对象
        self.paddle.draw_xzh(self.screen)
        self.ball.draw_xzh(self.screen)
        for brick in self.bricks:
            brick.draw_xzh(self.screen)

        # 绘制粒子效果
        for particle in self.particles:
            particle.draw(self.screen)

        # 绘制UI
        self.draw_ui_xzh()

        # 绘制提示信息
        if not self.game_started:
            self.draw_start_message_xzh()
        elif self.game_over:
            self.draw_game_over_message_xzh()
        elif self.game_won:
            self.draw_win_message_xzh()

        pygame.display.flip()

    def draw_background_xzh(self):
        """绘制渐变背景"""
        for i in range(SCREEN_HEIGHT):
            ratio = i / SCREEN_HEIGHT
            # 从深蓝到黑的渐变
            r = int(10 * (1 - ratio))
            g = int(20 * (1 - ratio))
            b = int(40 * (1 - ratio))
            pygame.draw.line(self.screen, (r, g, b), (0, i), (SCREEN_WIDTH, i))

    def draw_ui_xzh(self):
        """绘制游戏UI - 带半透明面板"""
        # 绘制左侧信息面板
        left_panel = pygame.Surface((150, 70), pygame.SRCALPHA)
        pygame.draw.rect(left_panel, (20, 40, 80, 180), (0, 0, 150, 70), border_radius=10)
        pygame.draw.rect(left_panel, (100, 150, 255, 100), (0, 0, 150, 70), 2, border_radius=10)
        self.screen.blit(left_panel, (5, 5))

        # 绘制分数
        score_text = self.font_small.render(f"分数: {self.score}", True, COLOR_WHITE_XZH)
        self.screen.blit(score_text, (15, 15))

        # 绘制生命值
        lives_text = self.font_small.render(f"生命: {self.lives}", True, COLOR_WHITE_XZH)
        self.screen.blit(lives_text, (15, 40))

        # 绘制右侧信息面板
        right_panel_width = 220
        right_panel = pygame.Surface((right_panel_width, 70), pygame.SRCALPHA)
        pygame.draw.rect(right_panel, (20, 40, 80, 180), (0, 0, right_panel_width, 70), border_radius=10)
        pygame.draw.rect(right_panel, (100, 150, 255, 100), (0, 0, right_panel_width, 70), 2, border_radius=10)
        self.screen.blit(right_panel, (SCREEN_WIDTH - right_panel_width - 5, 5))

        # 绘制模式和关卡（挑战模式显示关卡）
        if self.mode == MODE_CHALLENGE_XZH:
            mode_text = f"挑战模式 - 第{self.level}关"
        else:
            mode_text = "经典模式"
        mode_surface = self.font_small.render(mode_text, True, COLOR_YELLOW_XZH)
        self.screen.blit(mode_surface, (SCREEN_WIDTH - right_panel_width + 5, 15))

        # 绘制命中率
        if self.total_bricks_hit > 0:
            total = self.total_bricks_hit + self.total_bricks_missed
            hit_rate = (self.total_bricks_hit / total) * 100 if total > 0 else 0
            hit_text = self.font_small.render(f"命中率: {hit_rate:.1f}%", True, COLOR_GREEN_XZH)
            self.screen.blit(hit_text, (SCREEN_WIDTH - right_panel_width + 5, 40))

    def draw_start_message_xzh(self):
        """绘制开始提示信息 - 带半透明背景"""
        # 绘制半透明背景板
        overlay = pygame.Surface((600, 350), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (10, 20, 40, 220), (0, 0, 600, 350), border_radius=20)
        pygame.draw.rect(overlay, (100, 200, 255, 150), (0, 0, 600, 350), 3, border_radius=20)
        self.screen.blit(overlay, (SCREEN_WIDTH/2 - 300, SCREEN_HEIGHT/2 - 175))

        # 绘制文字（带阴影效果）
        title = self.font_large.render("打砖块游戏", True, COLOR_CYAN_XZH)
        title_shadow = self.font_large.render("打砖块游戏", True, (0, 0, 0))
        hint = self.font_medium.render("按空格键开始游戏", True, COLOR_WHITE_XZH)
        control1 = self.font_small.render("使用左右方向键或A/D键移动挡板", True, (200, 200, 200))
        control2 = self.font_small.render("按ESC键退出游戏", True, (200, 200, 200))

        # 绘制阴影
        self.screen.blit(title_shadow, (SCREEN_WIDTH/2 - title.get_width()/2 + 2, SCREEN_HEIGHT/2 - 98))
        # 绘制文字
        self.screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - 100))
        self.screen.blit(hint, (SCREEN_WIDTH/2 - hint.get_width()/2, SCREEN_HEIGHT/2))
        self.screen.blit(control1, (SCREEN_WIDTH/2 - control1.get_width()/2, SCREEN_HEIGHT/2 + 50))
        self.screen.blit(control2, (SCREEN_WIDTH/2 - control2.get_width()/2, SCREEN_HEIGHT/2 + 80))

    def draw_game_over_message_xzh(self):
        """绘制游戏结束信息 - 带半透明背景"""
        # 绘制半透明背景板
        panel_height = 300 if self.mode == MODE_CHALLENGE_XZH else 250
        overlay = pygame.Surface((500, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (40, 10, 10, 220), (0, 0, 500, panel_height), border_radius=20)
        pygame.draw.rect(overlay, (255, 100, 100, 150), (0, 0, 500, panel_height), 3, border_radius=20)
        self.screen.blit(overlay, (SCREEN_WIDTH/2 - 250, SCREEN_HEIGHT/2 - panel_height/2))

        # 绘制文字
        game_over_text = self.font_large.render("游戏结束", True, COLOR_RED_XZH)
        game_over_shadow = self.font_large.render("游戏结束", True, (0, 0, 0))
        score_text = self.font_medium.render(f"最终分数: {self.score}", True, COLOR_WHITE_XZH)

        # 挑战模式显示关卡信息
        if self.mode == MODE_CHALLENGE_XZH:
            level_text = self.font_medium.render(f"到达关卡: 第{self.level}关", True, COLOR_YELLOW_XZH)
            hint_text = self.font_small.render("按ESC键退出", True, (200, 200, 200))

            self.screen.blit(game_over_shadow, (SCREEN_WIDTH/2 - game_over_text.get_width()/2 + 2, SCREEN_HEIGHT/2 - 78))
            self.screen.blit(game_over_text, (SCREEN_WIDTH/2 - game_over_text.get_width()/2, SCREEN_HEIGHT/2 - 80))
            self.screen.blit(score_text, (SCREEN_WIDTH/2 - score_text.get_width()/2, SCREEN_HEIGHT/2 - 20))
            self.screen.blit(level_text, (SCREEN_WIDTH/2 - level_text.get_width()/2, SCREEN_HEIGHT/2 + 20))
            self.screen.blit(hint_text, (SCREEN_WIDTH/2 - hint_text.get_width()/2, SCREEN_HEIGHT/2 + 70))
        else:
            hint_text = self.font_small.render("按ESC键退出", True, (200, 200, 200))

            self.screen.blit(game_over_shadow, (SCREEN_WIDTH/2 - game_over_text.get_width()/2 + 2, SCREEN_HEIGHT/2 - 48))
            self.screen.blit(game_over_text, (SCREEN_WIDTH/2 - game_over_text.get_width()/2, SCREEN_HEIGHT/2 - 50))
            self.screen.blit(score_text, (SCREEN_WIDTH/2 - score_text.get_width()/2, SCREEN_HEIGHT/2 + 10))
            self.screen.blit(hint_text, (SCREEN_WIDTH/2 - hint_text.get_width()/2, SCREEN_HEIGHT/2 + 60))

    def draw_win_message_xzh(self):
        """绘制胜利信息 - 带半透明背景"""
        # 绘制半透明背景板
        overlay = pygame.Surface((500, 250), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (10, 40, 10, 220), (0, 0, 500, 250), border_radius=20)
        pygame.draw.rect(overlay, (100, 255, 100, 150), (0, 0, 500, 250), 3, border_radius=20)
        self.screen.blit(overlay, (SCREEN_WIDTH/2 - 250, SCREEN_HEIGHT/2 - 125))

        # 绘制文字（带阴影效果）
        win_text = self.font_large.render("恭喜获胜!", True, COLOR_GREEN_XZH)
        win_shadow = self.font_large.render("恭喜获胜!", True, (0, 0, 0))
        score_text = self.font_medium.render(f"最终分数: {self.score}", True, COLOR_WHITE_XZH)
        hint_text = self.font_small.render("按ESC键退出", True, (200, 200, 200))

        # 绘制阴影
        self.screen.blit(win_shadow, (SCREEN_WIDTH/2 - win_text.get_width()/2 + 2, SCREEN_HEIGHT/2 - 48))
        # 绘制文字
        self.screen.blit(win_text, (SCREEN_WIDTH/2 - win_text.get_width()/2, SCREEN_HEIGHT/2 - 50))
        self.screen.blit(score_text, (SCREEN_WIDTH/2 - score_text.get_width()/2, SCREEN_HEIGHT/2 + 10))
        self.screen.blit(hint_text, (SCREEN_WIDTH/2 - hint_text.get_width()/2, SCREEN_HEIGHT/2 + 60))

    def get_game_data_xzh(self):
        """
        获取游戏数据
        :return: 游戏数据字典
        """
        duration = 0
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time

        total_attempts = self.total_bricks_hit + self.total_bricks_missed
        hit_rate = (self.total_bricks_hit / total_attempts) if total_attempts > 0 else 0

        return {
            "mode": self.mode,
            "score": self.score,
            "level": self.level,  # 新增：关卡数
            "duration": duration,
            "hit_rate": hit_rate,
            "bricks_hit": self.total_bricks_hit,
            "lives_remaining": self.lives,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "won": self.game_won
        }

    def run_xzh(self):
        """运行游戏主循环"""
        try:
            while self.running:
                self.handle_events_xzh()
                self.update_xzh()
                self.draw_xzh()
                self.clock.tick(FPS)

            pygame.quit()
            return self.get_game_data_xzh()

        except Exception as e:
            print(f"游戏运行错误: {e}")
            pygame.quit()
            raise


def save_game_data_xzh(game_data):
    """
    保存游戏数据到JSON文件
    :param game_data: 游戏数据字典
    """
    try:
        # 读取现有数据
        try:
            with open(DATA_FILE_PATH_XZH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"games": []}

        # 添加新数据
        data["games"].append(game_data)

        # 保存数据
        with open(DATA_FILE_PATH_XZH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"游戏数据已保存到 {DATA_FILE_PATH_XZH}")

    except Exception as e:
        print(f"保存游戏数据错误: {e}")


def load_game_data_xzh():
    """
    从JSON文件加载游戏数据
    :return: 游戏数据列表
    """
    try:
        with open(DATA_FILE_PATH_XZH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("games", [])
    except FileNotFoundError:
        print("数据文件不存在，返回空列表")
        return []
    except Exception as e:
        print(f"加载游戏数据错误: {e}")
        return []
