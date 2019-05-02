# -*- coding: UTF-8 -*-     
import pygame
from objects import Object
from pygame.locals import *
from pygame import key
from pygame import time
from ammo import deltaAmmo
from ammo import Spawner
from ammo import Blast
from os import path
from los import Cast
import userevents
import xml.etree.ElementTree as ET

class Player(Object):
    def __init__(self, source, image, coords):
        Object.__init__(self, source, image, coords)
        self.source = source
        self.wallgroup = self.source.wallgroup
        self.wall_list = []
        for w in self.wallgroup.sprites():
            self.wall_list.append(w.rect)
        self.walls = self.wall_list
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
        self.speed = int(root.find("speed").text)
        self.velocity = 0.4
        self.ammo_speed = float(root.find("ammo_speed").text) * self.speed
        self.cooldown = int(root.find("cooldown").text)
        self.blast_cool = int(root.find("blast_cool").text)
        self.blast_radius = int(root.find("blast_radius").text)
        self.run_cool = int(root.find("run_cool").text)
        self.run_time = int(root.find("run_time").text)
        self.ammo_image = path.join("images", "ammo.png")
        self.ammogroup = pygame.sprite.Group()
        self.blastgroup = pygame.sprite.Group()
        self.aimx = lambda x : x #* self.speed
        self.aimy = lambda y : y #* self.speed
        #self.shoot_start = pygame.time.get_ticks() - self.cooldown
        #self.blast_start = pygame.time.get_ticks() - self.blast_cool
        self.run_start = pygame.time.get_ticks() - self.run_cool
        self.can_blast = True
        self.can_run = True
        self.run_speed = self.speed * 2
        self.old_dir = (1,0)
        self.old_ammo_dir = (0,0)
        self.ray_shrink = (-24,-6)
        self.cast = Cast(self)
        self.ammo_spawner = Spawner(self, deltaAmmo, self.cooldown, self.ammo_speed, self.ammo_image, 1, self.ammogroup)
        self.blast_spawner = Spawner(self, Blast, self.blast_cool, 1, self.ammo_image, 1, self.blastgroup)

    def turnaround(self, p):
        pass

    def updateWallgroup(self):
        self.wall_list = []
        for w in self.wallgroup.sprites():
            self.wall_list.append(w.rect)
        self.walls = self.wall_list
        self.cast = Cast(self)
    
    def update(self):
        testdir = self.cast.test(self.dir)
        self.dir = (self.dir[0] * testdir[0], self.dir[1] * testdir[1])
        self.rect = self.move_animator.goto(self.dir)

    def read_keys(self, keys):
        new_dir = (keys[0])
        if (new_dir != (0,0)):
            self.old_dir = new_dir
        self.dir = (new_dir[0] * self.speed, new_dir[1] * self.speed)
        if (keys[1] == "fire"):
            self.shoot()
        if (keys[1] == "blast"):
            self.blast()

    def read_mouse(self, mouse):
        if (mouse == (0,0)):
            self.blast()
        else:
            v1 = pygame.math.Vector2(self.get_pos())
            v2 = pygame.math.Vector2(mouse)
            v3 = v2 - v1
            print(v3)
            ammo_dir = (v3[0] * 90, v3[1] * 90)
            if (self.ammo_spawner.cast(ammo_dir)):
                pygame.event.post(userevents.player_shot_event())
            self.old_ammo_dir = ammo_dir


    def blast(self):
        ammo_dir = self.blast_radius
        if (self.blast_spawner.cast(ammo_dir)):
            pygame.event.post(userevents.player_blast_event())

    def shoot(self):
        if (self.dir == (0,0)):
            ammo_dir = (self.rect.centerx - self.old_dir[0] * -100, self.rect.centery - self.old_dir[1] * -100)
        else:
            ammo_dir = (self.rect.centerx - self.dir[0] * -100, self.rect.centery - self.dir[1] * -100)
        if (self.ammo_spawner.cast(ammo_dir)):
            pygame.event.post(userevents.player_shot_event())
        self.dir = (0,0)
        self.old_ammo_dir = ammo_dir


    def destroy(self):
        self.source.player_items["speed"] = self.speed
        self.source.player_items["blast_radius"] = self.blast_radius
        self.source.player_items["shots_n"] = self.ammo_spawner.shots_n
        self.dir = (0,0)
        self.alive = False
        self.kill()
        del self
        pygame.event.post(userevents.player_died())

    def set_items(self, items):
        self.speed = items["speed"]
        self.ammo_spawner.shots_n = items["shots_n"]
        self.blast_radius = items["blast_radius"]

