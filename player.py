# -*- coding: UTF-8 -*-     
import pygame
from objects import Object
from pygame.locals import *
from pygame import key
from pygame import time
from pygame.math import Vector2
from ammo import Ammo
from os import path

class Player(Object):
    def __init__(self, screen, image, coords, size):
        Object.__init__(self, screen, image, coords, size)
        self.speed = 1.5
        self.clk = time.Clock()
        self.ammo_image = path.join("images", "ammo.png")
        self.ammogroup = pygame.sprite.Group()
        self.aimx = lambda x : x * self.speed
        self.aimy = lambda y : y * self.speed
        self.old_dir = (1,0)
        self.keyh = {
                    K_RIGHT: self.aimx(1),
                    K_LEFT: self.aimx(-1),
                    }
        self.keyv = {
                    K_UP: self.aimy(-1),
                    K_DOWN: self.aimy(1)
                    }
        self.keya = {
                    K_z: Ammo 
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
        if (self.dir != (0,0)):
            self.old_dir = self.dir
        for k, v in self.keya.items():
            if (pressed[k]):
                pew = self.keya[k](self.screen, self.ammo_image, (self.rect[0], self.rect[1]), self.old_dir, 4)
                self.ammogroup.add(pew)



