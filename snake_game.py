import pygame
import random
import sys
import os

# 初始化Pygame
pygame.init()

# 定義常量
寬度, 高度 = 800, 600
蛇_大小 = 20
初始速度 = 5
最大速度 = 15
FPS = 60

# 定義顏色
白色 = (255, 255, 255)
黑色 = (0, 0, 0)
紅色 = (255, 99, 71)
綠色 = (50, 205, 50)
背景色 = (240, 255, 240)
分數顏色 = (0, 0, 139)

# 設置遊戲窗口
窗口 = pygame.display.set_mode((寬度, 高度))
pygame.display.set_caption('Snake Game')

# 定義字體
大字體 = pygame.font.Font(None, 50)
小字體 = pygame.font.Font(None, 25)

class 蛇:
    def __init__(self):
        self.重置()

    def 重置(self):
        self.x = 寬度 // 2
        self.y = 高度 // 2
        self.身體 = [[self.x, self.y]]
        self.長度 = 1
        self.方向 = [0, 0]
        self.新方向 = [0, 0]

    def 移動(self):
        # 更新方向
        if self.新方向 != [0, 0]:
            self.方向 = self.新方向

        # 移動蛇頭
        self.x += self.方向[0]
        self.y += self.方向[1]
        
        # 更新蛇身
        self.身體.insert(0, [self.x, self.y])
        if len(self.身體) > self.長度:
            self.身體.pop()

    def 改變方向(self, 新方向):
        # 檢查是否與當前方向相反
        if (新方向[0] * -1, 新方向[1] * -1) != tuple(self.方向):
            self.新方向 = 新方向

    def 檢查碰撞(self):
        # 檢查是否碰到邊界
        if (self.x < 0 or self.x >= 寬度 or
            self.y < 0 or self.y >= 高度):
            return True
        
        # 檢查是否碰到自己的身體
        for 部分 in self.身體[1:]:
            if self.x == 部分[0] and self.y == 部分[1]:
                return True
        
        return False

    def 吃到食物(self, 食物):
        return self.x == 食物.x and self.y == 食物.y

    def 畫(self, 窗口):
        for 部分 in self.身體:
            pygame.draw.rect(窗口, 綠色, [部分[0], 部分[1], 蛇_大小, 蛇_大小])

class 食物:
    def __init__(self):
        self.重置位置()

    def 重置位置(self):
        self.x = round(random.randrange(0, 寬度 - 蛇_大小) / 蛇_大小) * 蛇_大小
        self.y = round(random.randrange(0, 高度 - 蛇_大小) / 蛇_大小) * 蛇_大小

    def 畫(self, 窗口):
        pygame.draw.rect(窗口, 紅色, [self.x, self.y, 蛇_大小, 蛇_大小])

class 遊戲:
    def __init__(self):
        self.蛇 = 蛇()
        self.食物 = 食物()
        self.分數 = 0
        self.速度 = 初始速度
        self.最高分 = self.讀取最高分()
        self.移動計時器 = 0
        self.移動間隔 = 200  # 初始移動間隔（毫秒）

    def 讀取最高分(self):
        最高分文件 = 'high_score.txt'
        if os.path.exists(最高分文件):
            with open(最高分文件, 'r') as f:
                return int(f.read())
        return 0

    def 保存最高分(self):
        with open('high_score.txt', 'w') as f:
            f.write(str(self.最高分))

    def 重置(self):
        self.蛇.重置()
        self.食物.重置位置()
        self.分數 = 0
        self.速度 = 初始速度
        self.移動間隔 = 200

    def 更新(self, dt):
        self.移動計時器 += dt
        if self.移動計時器 >= self.移動間隔:
            self.蛇.移動()
            self.移動計時器 = 0

            if self.蛇.吃到食物(self.食物):
                self.蛇.長度 += 1
                self.分數 += 10
                self.食物.重置位置()
                self.移動間隔 = max(50, self.移動間隔 - 5)  # 每次吃到食物，移動間隔減少5毫秒，但不少於50毫秒

            if self.分數 > self.最高分:
                self.最高分 = self.分數
                self.保存最高分()

    def 畫(self):
        窗口.fill(背景色)
        self.蛇.畫(窗口)
        self.食物.畫(窗口)
        self.顯示分數()
        pygame.display.update()

    def 顯示分數(self):
        最高分文字 = 小字體.render(f"High Score: {self.最高分}", True, 分數顏色)
        分數文字 = 小字體.render(f"Score: {self.分數}", True, 分數顏色)
        窗口.blit(最高分文字, [10, 10])
        窗口.blit(分數文字, [10, 40])

    def 遊戲結束畫面(self):
        窗口.fill(背景色)
        顯示消息("Game Over", 紅色, 大字體, -30)
        顯示消息(f"Final Score: {self.分數}", 分數顏色, 小字體, 30)
        顯示消息("Press SPACE to play again or ESC to quit", 黑色, 小字體, 80)
        pygame.display.update()

def 顯示消息(消息, 顏色, 字體, y_偏移=0):
    文字 = 字體.render(消息, True, 顏色)
    文字矩形 = 文字.get_rect()
    文字矩形.center = (寬度 // 2, 高度 // 2 + y_偏移)
    窗口.blit(文字, 文字矩形)

def 主循環():
    遊戲實例 = 遊戲()
    時鐘 = pygame.time.Clock()

    while True:
        dt = 時鐘.tick(FPS)
        for 事件 in pygame.event.get():
            if 事件.type == pygame.QUIT:
                return False
            if 事件.type == pygame.KEYDOWN:
                if 事件.key == pygame.K_LEFT:
                    遊戲實例.蛇.改變方向([-蛇_大小, 0])
                elif 事件.key == pygame.K_RIGHT:
                    遊戲實例.蛇.改變方向([蛇_大小, 0])
                elif 事件.key == pygame.K_UP:
                    遊戲實例.蛇.改變方向([0, -蛇_大小])
                elif 事件.key == pygame.K_DOWN:
                    遊戲實例.蛇.改變方向([0, 蛇_大小])

        遊戲實例.更新(dt)

        if 遊戲實例.蛇.檢查碰撞():
            遊戲實例.遊戲結束畫面()
            等待回應 = True
            while 等待回應:
                for 事件 in pygame.event.get():
                    if 事件.type == pygame.QUIT:
                        return False
                    if 事件.type == pygame.KEYDOWN:
                        if 事件.key == pygame.K_SPACE:
                            遊戲實例.重置()
                            等待回應 = False
                        elif 事件.key == pygame.K_ESCAPE:
                            return False

        遊戲實例.畫()

    return True

if __name__ == "__main__":
    主循環()
    pygame.quit()
    sys.exit()