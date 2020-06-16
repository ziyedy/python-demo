import pygame
import sys
from cfg import *
from plane import Hero, Enemy
from utils import Button, Result


class Game:
    """ 游戏运行主类 """

    # 状态变量
    READY = 0
    START = 1
    OVER = -1
    status = READY

    btn_start_index = 0

    frame = 0
    clock = pygame.time.Clock()

    def __init__(self):
        """ 游戏初始化 """
        pygame.init()
        self.screen = pygame.display.set_mode(WIN_SIZE)
        pygame.display.set_caption("飞机大战")

        self.img_bg = pygame.image.load(IMG_BG)
        self.hero = Hero(self.screen)
        self.enemies = self.get_enemies(5)

        self.result = Result()

        self.btn_enter = [Button(BTN_ENTER1), Button(BTN_ENTER2)]

        self.score_font = pygame.font.SysFont('宋体', 45)

    def get_enemies(self, num):
        """
        获取敌人精灵组
        :return: 敌人精灵组
        """
        Enemies = pygame.sprite.Group()
        for i in range(num):
            enemy = Enemy(self.screen)
            Enemies.add(enemy)
        return Enemies

    def event_listen(self):
        """ 事件监听 """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.status == self.START and event.key == pygame.K_SPACE:
                    self.hero.shoot()
                if self.status == self.OVER and event.key == pygame.K_SPACE:
                    self.status = self.READY
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.status == self.READY and self.btn_enter[0].judge_mouse(mouse):
                    self.btn_start_index = 1
                    self.status = self.START
            if event.type == pygame.MOUSEMOTION:
                mouse = pygame.mouse.get_pos()
                if self.status == self.READY and self.btn_enter[0].judge_mouse(mouse):
                    self.btn_start_index = 1
                else:
                    self.btn_start_index = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.hero.move("left")
        if keys[pygame.K_d]:
            self.hero.move("right")
        if keys[pygame.K_w]:
            self.hero.move("top")
        if keys[pygame.K_s]:
            self.hero.move("down")

    def run_game(self):
        """ 游戏主循环 """
        while True:

            self.clock.tick(40)
            self.frame += 1
            if self.frame >= 200:
                self.frame = 0
                enemy = Enemy(self.screen)
                self.enemies.add(enemy)

            self.event_listen()

            if self.status == self.READY:
                self.screen.blit(self.img_bg, self.img_bg.get_rect())
                self.screen.blit(self.btn_enter[self.btn_start_index].image, self.btn_enter[0].rect)
                max_score_text = self.score_font.render('Max scores:{0}'.format(self.result.get_max_score()), True, RED)
                self.screen.blit(max_score_text, [0, 0])

            elif self.status == self.START:
                self.screen.blit(self.img_bg, self.img_bg.get_rect())
                score_text = self.score_font.render('Scores:{0}'.format(self.result.score), True, RED)
                blood_text = self.score_font.render('Blood:{}'.format(self.result.blood), True, RED)
                self.screen.blit(score_text, [0, 5])
                self.screen.blit(blood_text, [0, 45])

                self.hero.update()
                self.hero.bullets.update(self.enemies, self.result)
                self.enemies.update(self.result)

                if pygame.sprite.spritecollide(self.hero, self.enemies, False) or self.result.blood <= 0:
                    self.enemies.empty()
                    self.hero.broken()

                    self.result.set_max_score()

                    self.status = self.OVER

            elif self.status == self.OVER:
                self.screen.blit(self.img_bg, self.img_bg.get_rect())
                score_text = self.score_font.render('Scores:{0}'.format(self.result.score), True, RED)
                max_score_text = self.score_font.render('Max scores:{0}'.format(self.result.get_max_score()), True, RED)
                tip_text = self.score_font.render('Press the Space to continue!', True, RED)
                self.screen.blit(score_text, (WIN_SIZE[0]/2-70, WIN_SIZE[1]/2-40))
                self.screen.blit(max_score_text, (WIN_SIZE[0]/2-100, WIN_SIZE[1]/2-90))
                self.screen.blit(tip_text, (WIN_SIZE[0]/2-200, WIN_SIZE[1]/2-135))

            # 刷新屏幕
            pygame.display.update()
