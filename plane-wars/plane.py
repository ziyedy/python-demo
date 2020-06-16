import pygame
from cfg import *
from random import randint


class Bullet(pygame.sprite.Sprite):
    """ 子弹类 """
    speed = 12

    def __init__(self, screen, plane):
        """ 初始化子弹相关信息 """
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load(IMG_BULLET)
        self.plane = plane
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plane.rect.centerx
        self.rect.top = self.plane.rect.top

    def draw(self):
        """ 绘制子弹 """
        self.screen.blit(self.image, self.rect)

    def update(self, enemy, result):
        """ 更新子弹状态 """
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.remove(self.plane.bullets)
        self.draw()
        res = pygame.sprite.spritecollide(self, enemy, False)
        for r in res:
            self.kill()
            r.collide(result)


class Hero(pygame.sprite.Sprite):
    """ 我方飞机类 """

    speed = 6
    bullets = pygame.sprite.Group()

    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load(IMG_HERO)
        self.width, self.height = self.image.get_size()
        self.rect = self.get_pos()

        self.img_broken1 = pygame.image.load(IMG_BROKEN1)
        self.img_broken2 = pygame.image.load(IMG_BROKEN2)
        self.img_broken3 = pygame.image.load(IMG_BROKEN3)

        self.muc_shoot = pygame.mixer.Sound(MUC_BULLET)
        self.muc_over = pygame.mixer.Sound(MUC_GAME_OVER)

    def get_pos(self):
        """ 初始化英雄位置（居中） """
        rect = self.image.get_rect()
        rect.left = int((WIN_SIZE[0] - self.width) / 2)
        rect.top = int((WIN_SIZE[1] - self.height) / 2)
        return rect

    def update(self):
        """ 更新状态 """
        self.draw()

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def move(self, direct):
        """ 飞机移动 """
        if direct == "left":
            self.rect.left -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
        elif direct == 'right':
            self.rect.left += self.speed
            if self.rect.left >= WIN_SIZE[0] - self.width:
                self.rect.left = WIN_SIZE[0] - self.width
        elif direct == 'top':
            self.rect.top -= self.speed
            if self.rect.top < 0:
                self.rect.top = 0
        elif direct == 'down':
            self.rect.top += self.speed
            if self.rect.top >= WIN_SIZE[1] - self.height:
                self.rect.top = WIN_SIZE[1] - self.height

    def shoot(self):
        """ 发射子弹 """
        self.muc_shoot.play()
        bullet = Bullet(self.screen, self)
        self.bullets.add(bullet)

    def broken(self):
        """ 飞机坠毁 """
        self.screen.blit(self.img_broken1, self.rect)
        self.screen.blit(self.img_broken2, self.rect)
        self.screen.blit(self.img_broken3, self.rect)
        self.muc_over.play()


class Enemy(pygame.sprite.Sprite):
    """ 敌机类 """
    speed = 5
    blood = 8
    point = 10

    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        if randint(-2, 2) > 0:
            self.image = pygame.image.load(IMG_ENEMY1)
            self.speed = 7
            self.blood = 4
            self.point = 5
        else:
            self.image = pygame.image.load(IMG_ENEMY2)
        self.rect = self.image.get_rect()
        self.init_pos()

        self.img_broken1 = pygame.image.load(IMG_BROKEN1)
        self.img_broken2 = pygame.image.load(IMG_BROKEN2)
        self.img_broken3 = pygame.image.load(IMG_BROKEN3)

        self.muc_enemy_down = pygame.mixer.Sound(MUC_ENEMY_DOWN)

    def init_pos(self):
        """ 初始化飞机位置 """
        self.rect.left = randint(0, 300)
        self.rect.top = randint(-500, -200)

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self, result):
        self.rect.top += self.speed
        self.draw()
        if self.rect.top >= WIN_SIZE[1]:
            result.blood = self.point
            self.init_pos()

    def collide(self, result):
        """ 碰撞后血量降低，到0后坠毁 """
        self.blood -= 4
        if self.blood <= 0:
            self.broken(result)

    def broken(self, result):
        """ 敌机坠毁相应事件 """
        result.score = self.point
        self.screen.blit(self.img_broken1, self.rect)
        self.screen.blit(self.img_broken2, self.rect)
        self.screen.blit(self.img_broken3, self.rect)
        self.muc_enemy_down.play()
        self.init_pos()
