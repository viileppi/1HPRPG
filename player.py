# -*- coding: UTF-8 -*-     
import pygame
from objects import Object
from pygame.locals import *
from pygame import key
from pygame import time
from ammo import deltaAmmo
from ammo import Blast
from os import path
from los import Cast
import keymap

class Player(Object):
    def __init__(self, screen, image, coords, size, wallgroup, keymap_i):
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
        self.blast_cool = 1000
        self.old_dir = (1,0)
        self.cast = Cast(self.screen, self.wall_list, self)
        self.keymap_i = keymap_i
        self.keyh = keymap.keymaps[self.keymap_i]["keyh"]
        self.keyv = keymap.keymaps[self.keymap_i]["keyv"]
        self.keya = keymap.keymaps[self.keymap_i]["keya"]
        # self.keyh = {
        #             K_RIGHT: self.aimx(1),
        #             K_LEFT: self.aimx(-1),
        #             }
        # self.keyv = {
        #             K_UP: self.aimy(-1),
        #             K_DOWN: self.aimy(1)
        #             }
        # self.keya = {
        #             K_z: deltaAmmo, 
        #             K_x: Blast
        #             }

    def turnaround(self, p):
        pass

    def read_keys(self, pressed):
        self.cast.walls = self.wall_list.sprites()
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
            testdir = self.cast.test(self.dir)
            self.dir = (self.dir[0] * testdir[0], self.dir[1] * testdir[1])
        for k, v in self.keya.items():
            if (pressed[k] and self.keya[k] == deltaAmmo):
                self.dir = (0,0)
                if (((pygame.time.get_ticks() - self.shoot_start) > self.cooldown)):
                    ammo_dir = (self.rect.centerx - self.old_dir[0] * -100, self.rect.centery - self.old_dir[1] * -100)
                    pew = self.keya[k](self.screen, self.ammo_image, self.get_pos(), ammo_dir, 3)
                    self.ammogroup.add(pew)
                    self.dir = (0,0)
                    self.move_animator.rect = self.move_animator.crop_init
                    self.shoot_start = pygame.time.get_ticks()
            if (pressed[k] and self.keya[k] == Blast):
                if (((pygame.time.get_ticks() - self.shoot_start) > self.blast_cool)):
                    blast = self.keya[k](self.screen, self, 192)
                    self.ammogroup.add(blast)
                    self.shoot_start = pygame.time.get_ticks()

    def change_keymap(self, keymap_i):
        self.keymap_i = keymap_i
        self.keyh = keymap.keymaps[self.keymap_i]["keyh"]
        self.keyv = keymap.keymaps[self.keymap_i]["keyv"]
        self.keya = keymap.keymaps[self.keymap_i]["keya"]

