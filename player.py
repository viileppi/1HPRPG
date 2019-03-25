# -*- coding: UTF-8 -*-     
import pygame
from objects import Object
from pygame.locals import *
from pygame import key
from pygame import time
from ammo import deltaAmmo
from os import path

class Player(Object):
    def __init__(self, screen, image, coords, size, wallgroup):
        Object.__init__(self, screen, image, coords, size)
        self.wallgroup = wallgroup
        self.wall_list = []
        for w in self.wallgroup.sprites():
            self.wall_list.append(w.rect)
        self.speed = 1.5
        self.clk = time.Clock()
        self.ammo_image = path.join("images", "ammo.png")
        self.ammogroup = pygame.sprite.Group()
        self.aimx = lambda x : x * self.speed
        self.aimy = lambda y : y * self.speed
        self.shoot_start = pygame.time.get_ticks()
        self.cooldown = 500
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
                    K_z: deltaAmmo 
                    }

    def turnaround(self, p):
        self.dir = (self.old_dir[0] * -1, self.old_dir[1] * -1)
        self.update()

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
            cr = self.rect.move(self.dir)
            lc = cr.collidelistall(self.wall_list)
            if (len(lc) > 0):
                self.dir = (0,0)
        for k, v in self.keya.items():
            if (pressed[k]):
                if (((pygame.time.get_ticks() - self.shoot_start) > self.cooldown)):
                    ammo_dir = (self.rect.centerx - self.old_dir[0] * -100, self.rect.centery - self.old_dir[1] * -100)
                    pew = self.keya[k](self.screen, self.ammo_image, self.get_pos(), ammo_dir, 16)
                    self.ammogroup.add(pew)
                    self.dir = (0,0)
                    self.move_animator.rect = self.move_animator.crop_init
                    self.shoot_start = pygame.time.get_ticks()
