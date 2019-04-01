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
import userevents

class Player(Object):
    def __init__(self, screen, image, coords, size, wallgroup, keymap_i):
        Object.__init__(self, screen, image, coords, size)
        self.wallgroup = wallgroup
        self.wall_list = []
        for w in self.wallgroup.sprites():
            self.wall_list.append(w.rect)
        self.speed = 2
        self.ammo_speed = 3
        self.clk = time.Clock()
        self.ammo_image = path.join("images", "ammo.png")
        self.ammogroup = pygame.sprite.Group()
        self.blastgroup = pygame.sprite.Group()
        self.aimx = lambda x : x * self.speed
        self.aimy = lambda y : y * self.speed
        self.cooldown = 250
        self.blast_cool = 2000
        self.shoot_start = pygame.time.get_ticks() - self.cooldown
        self.blast_start = pygame.time.get_ticks() - self.blast_cool
        self.can_blast = True
        self.old_dir = (1,0)
        self.cast = Cast(self.screen, self.wall_list, self)
        self.keymap_i = keymap_i
        # self.keyh = keymap.keymaps[self.keymap_i]["keyh"]
        # self.keyv = keymap.keymaps[self.keymap_i]["keyv"]
        # self.keya = keymap.keymaps[self.keymap_i]["keya"]
        self.keyh = {
                    K_RIGHT: self.aimx(1),
                    K_LEFT: self.aimx(-1),
                    }
        self.keyv = {
                    K_UP: self.aimy(-1),
                    K_DOWN: self.aimy(1)
                    }
        self.keya = {
                    K_f: deltaAmmo, 
                    K_d: Blast
                    }

    def turnaround(self, p):
        self.dir = (self.dir[0] * -1, self.dir[1] * -1)

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
                if (((pygame.time.get_ticks() - self.shoot_start) > self.cooldown)):
                    ammo_dir = (self.rect.centerx - self.old_dir[0] * -100, self.rect.centery - self.old_dir[1] * -100)
                    ammo_start = (self.rect.centerx - self.old_dir[0] * -10, self.rect.centery - self.old_dir[1] * -10)
                    pew = self.keya[k](self.screen, self.ammo_image, ammo_start, ammo_dir, self.ammo_speed)
                    self.ammogroup.add(pew)
                    self.shoot_start = pygame.time.get_ticks()
                    pygame.event.post(userevents.player_shot_event())
                self.dir = (0,0)
            if (pressed[k] and self.keya[k] == Blast):
                if (((pygame.time.get_ticks() - self.blast_start) > self.blast_cool)):
                    blast = self.keya[k](self.screen, self, 72)
                    self.blastgroup.add(blast)
                    self.blast_start = pygame.time.get_ticks()
                    self.can_blast = False
                    pygame.event.post(userevents.player_blast_event())
        if (not self.can_blast and ((pygame.time.get_ticks() - self.blast_start) > self.blast_cool)):
            self.can_blast = True

    def change_keymap(self, keymap_i):
        self.keymap_i = keymap_i
        self.keyh = keymap.keymaps[self.keymap_i]["keyh"]
        self.keyv = keymap.keymaps[self.keymap_i]["keyv"]
        self.keya = keymap.keymaps[self.keymap_i]["keya"]

    def destroy(self):
        self.dir = (0,0)
        self.alive = False
        self.kill()
        del self
        pygame.event.post(userevents.player_died())


