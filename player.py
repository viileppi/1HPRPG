# -*- coding: UTF-8 -*-     
from objects import Object
from pygame.locals import *
from pygame import key
from pygame import time

class Player(Object):
    def __init__(self, screen, image, coords, size):
        Object.__init__(self, screen, image, coords, size)
        self.speed = 1.5
        self.clk = time.Clock()
        self.aimx = lambda x : x * self.speed
        self.aimy = lambda y : y * self.speed
        self.keyh = {
                    K_RIGHT: self.aimx(1),
                    K_LEFT: self.aimx(-1),
                    }
        self.keyv = {
                    K_UP: self.aimy(-1),
                    K_DOWN: self.aimy(1)
                    }


    def read_keys(self, pressed):
        self.dir = (0,0)
        x = 0
        y = 0
        for k, v in self.keyh.items():
            if (pressed[k]):
                x = self.keyh[k]
        for k, v in self.keyv.items():
            if (pressed[k]):
                y = self.keyv[k]
        self.dir = (x,y)



