# -*- coding: UTF-8 -*-     
import objects
import pygame
from ammo import Ammo
from ammo import deltaAmmo
from los import LOS
from os import path
from pygame.math import Vector2

class Enemy(objects.Object):
    def __init__(self, screen, image, coords, size, player, wall_group, ammogroup):
        """ image should be a spritesheet of square sprites """
        objects.Object.__init__(self, screen, image, coords, size)
        self.forward = True
        self.walked = 0
        self.walk_dist = 100
        self.where = (1,0)
        self.player = player
        self.wall_group = wall_group
        self.ammo_image = path.join("images", "ammo.png")
        self.ammogroup = ammogroup
        self.los = LOS(self.screen, self.get_pos(), self.player, self.wall_group)
        self.seen_player = False
        self.shoot_start = pygame.time.get_ticks()
        self.cooldown = 500
        self.ammo_speed = 5

    def seek(self):
        if (self.seen_player):
            self.where = (0,0)
            p = self.player.get_pos()
            e = self.get_pos()
            # v1 = Vector2(p)
            # v2 = Vector2(e)
            # v3 = v1 - v2
            # print(v3.normalize())
            if (((pygame.time.get_ticks() - self.shoot_start) > self.cooldown)):
                    pew = deltaAmmo(self.screen, self.ammo_image, e, p, self.ammo_speed)
                    self.ammogroup.add(pew)
                    self.shoot_start = pygame.time.get_ticks()
        self.walked += 1
        if (self.walked > self.walk_dist):
            self.turnaround(0)
            self.walked = 0


    def turnaround(self, point):
        self.forward = not self.forward
        # self.walked = 1
        if (self.where == (1,0)):
            self.where = (0,1)
        elif (self.where == (0,1)):
            self.where = (-1,0)
        elif (self.where == (0,-1)):
            self.where = (1,0)
        elif (self.where == (-1,0)):
            self.where = (0,-1)
        elif (self.where == (0,0)):
            self.where = (1,0)
        self.move((self.where[0] * 4, self.where[1] * 4))

    def update(self):
        self.seen_player = self.los.draw(self.get_pos())
        self.seek()
        self.rect = self.move_animator.goto(self.where)
