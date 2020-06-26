"""
定义游戏的一些固定参数
"""

import os
import pygame

# 根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 资源目录
SRC_DIR = os.path.join(BASE_DIR, 'src')

# 窗口大小
WIN_SIZE = (512, 768)

# 进入按钮
BTN_ENTER1 = os.path.join(SRC_DIR, 'imgs/button1.tga')
BTN_ENTER2 = os.path.join(SRC_DIR, 'imgs/button2.tga')

# 背景图片
IMG_BG = os.path.join(SRC_DIR, 'imgs/background.png')

# Hero图片
IMG_HERO = os.path.join(SRC_DIR, 'imgs/hero.png')


# 子弹图片
IMG_BULLET = os.path.join(SRC_DIR, 'imgs/bullet.png')

# 敌人图片
IMG_ENEMY1 = os.path.join(SRC_DIR, 'imgs/enemy1.png')
IMG_ENEMY2 = os.path.join(SRC_DIR, 'imgs/enemy2.png')

# 摧毁图片
IMG_BROKEN1 = os.path.join(SRC_DIR, 'imgs/broken1.png')
IMG_BROKEN2 = os.path.join(SRC_DIR, 'imgs/broken2.png')
IMG_BROKEN3 = os.path.join(SRC_DIR, 'imgs/broken3.png')

# 颜色
RED = pygame.Color(255, 0, 255)

# 音乐
MUC_BULLET = os.path.join(SRC_DIR, 'sounds/bullet.wav')
MUC_ENEMY_DOWN = os.path.join(SRC_DIR, 'sounds/enemy_down.wav')
MUC_GAME_OVER = os.path.join(SRC_DIR, 'sounds/game_over.wav')

# 字体
FONT = os.path.join(SRC_DIR, 'Gabriola.ttf')

# 游戏结果存储
GAME_RECORD = os.path.join(SRC_DIR, 'record.txt')