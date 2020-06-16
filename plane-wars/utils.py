import pygame
from cfg import *


class Button(pygame.sprite.Sprite):
    """ 按钮类，记录按键信息 """

    def __init__(self, path):
        """
        初始化函数
        :param path: 按钮图片文件路径
        """
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.set_pos()

    def set_pos(self):
        width, height = self.image.get_size()
        rect = self.image.get_rect()
        rect.left = int((WIN_SIZE[0] - width) / 2)
        rect.top = int((WIN_SIZE[1] - height) / 2)
        return rect

    def judge_mouse(self, mouse):
        """
        用于判断鼠标是否在按钮之上
        :param mouse: 鼠标所处的位置
        :return: 布尔值，判断是否在按钮之上
        """
        if (mouse[0] > self.rect.topleft[0]) and (mouse[0] < self.rect.bottomright[0]) \
                and (mouse[1] > self.rect.topleft[1]) and (mouse[1] < self.rect.bottomright[1]):
            return True
        else:
            return False


class Result(object):
    """ 用于记录游戏结果 """

    __score = 0
    __blood = 50

    @property
    def score(self):
        """ 游戏分数 """
        return self.__score

    @score.setter
    def score(self, value):
        """ 设置游戏分数 """
        self.__score += value

    @property
    def blood(self):
        """ 基地血量 """
        return self.__blood

    @blood.setter
    def blood(self, value):
        """ 设置基地血量 """
        self.__blood -= value

    def get_max_score(self):
        """ 读取历史最高分 """
        res = 0
        with open(GAME_RECORD, 'r') as f:
            r = f.read()
            if r:
                res = r
        res = int(res)
        return res

    def set_max_score(self):
        """ 记录最高分 """
        max_score = self.get_max_score()
        if self.score > max_score:
            with open(GAME_RECORD, 'w') as f:
                f.write('{0}'.format(self.score))





