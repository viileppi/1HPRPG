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
import xml.etree.ElementTree as ET

class Player(Object):
    def __init__(self, screen, image, coords, wallgroup, keymap_i):
        Object.__init__(self, screen, image, coords)
        self.wallgroup = wallgroup
        self.wall_list = []
        for w in self.wallgroup.sprites():
            self.wall_list.append(w.rect)
        """ # old settings for sanity
        self.speed = 2
        self.ammo_speed = 3
        self.cooldown = 250
        self.blast_cool = 2000
        self.run_cool = 3000
        self.run_time = 750
        """
        tree = ET.parse("settings.xml")
        root = tree.getroot().find("player")
        fps = int(tree.getroot().find("main").find("fps").text)
        self.speed = int(root.find("speed").text) * (fps/100)
        self.ammo_speed = float(root.find("ammo_speed").text) * self.speed
        self.cooldown = int(root.find("cooldown").text)
        self.blast_cool = int(root.find("blast_cool").text)
        self.blast_radius = int(root.find("blast_radius").text)
        self.run_cool = int(root.find("run_cool").text)
        self.run_time = int(root.find("run_time").text)
        self.ammo_image = path.join("images", "ammo.png")
        self.ammogroup = pygame.sprite.Group()
        self.blastgroup = pygame.sprite.Group()
        self.aimx = lambda x : x * self.speed
        self.aimy = lambda y : y * self.speed
        self.shoot_start = pygame.time.get_ticks() - self.cooldown
        self.blast_start = pygame.time.get_ticks() - self.blast_cool
        self.run_start = pygame.time.get_ticks() - self.run_cool
        self.can_blast = True
        self.can_run = True
        self.old_dir = (1,0)
        self.cast = Cast(self.screen, self.wall_list, self)
        self.keymap_i = keymap_i
        tree = ET.parse("keymap.xml")
        root = tree.getroot()
        kd = {}
        for keycode in root.findall("key"):
            value = int(keycode.find("value").text)
            name = keycode.get("name")
            kd[name] = value
        self.keyh = {
                    kd["right"]: self.aimx(1),
                    kd["left"]: self.aimx(-1),
                    }
        self.keyv = {
                    kd["up"]: self.aimy(-1),
                    kd["down"]: self.aimy(1)
                    }
        self.keya = {
                    kd["fire"]: deltaAmmo, 
                    kd["blast"]: Blast,
                    kd["run"]: "run"
                    }

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
                if (((pygame.time.get_ticks() - self.shoot_start) > self.cooldown)):
                    ammo_dir = (self.rect.centerx - self.old_dir[0] * -100, self.rect.centery - self.old_dir[1] * -100)
                    ammo_start = (self.rect.centerx - self.old_dir[0] * -5, self.rect.centery - self.old_dir[1] * -5)
                    pew = self.keya[k](self.screen, self.ammo_image, ammo_start, ammo_dir, self.ammo_speed)
                    self.ammogroup.add(pew)
                    self.shoot_start = pygame.time.get_ticks()
                    pygame.event.post(userevents.player_shot_event())
                self.dir = (0,0)
            if (pressed[k] and self.keya[k] == Blast):
                if (((pygame.time.get_ticks() - self.blast_start) > self.blast_cool)):
                    blast = self.keya[k](self.screen, self, self.blast_radius)
                    self.blastgroup.add(blast)
                    self.blast_start = pygame.time.get_ticks()
                    self.can_blast = False
                    pygame.event.post(userevents.player_blast_event())
            if (pressed[k] and self.keya[k] == "run"):
                if (((pygame.time.get_ticks() - self.run_start) > self.run_cool)):
                    self.run_start = pygame.time.get_ticks()
                    self.dir = (self.dir[0] * 2, self.dir[1] * 2)
                    self.can_run = False
        if (not self.can_blast and ((pygame.time.get_ticks() - self.blast_start) > self.blast_cool)):
            self.can_blast = True
        if (not self.can_run and ((pygame.time.get_ticks() - self.run_start) > self.run_cool)):
            self.can_run = True
        if (((pygame.time.get_ticks() - self.run_start) < self.run_time)):
            self.dir = (self.dir[0] * 2, self.dir[1] * 2)

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


