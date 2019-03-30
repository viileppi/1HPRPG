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
        self.speed = 1
        self.walked = 0
        self.walk_dist = 100
        self.where = (1,0)
        self.player = player
        self.wall_group = wall_group
        self.ammo_image = path.join("images", "ammo.png")
        self.ammogroup = ammogroup
        self.los = LOS(self.screen, self.get_pos(), self.player, self.wall_group)
        self.seen_player = False
        self.ready = False
        self.shoot_start = pygame.time.get_ticks()
        self.boot_start = pygame.time.get_ticks()
        self.ammo_speed = 3
        self.boot_time = 1000
        self.cooldown = 500
        self.image_backup = self.image.copy()
        self.divider = self.rect.height

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
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT + 4))
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
        self.move((self.where[0] * self.speed, self.where[1] * self.speed))

    def update(self):
        if (self.ready):
            self.seen_player = self.los.draw(self.get_pos())
            self.seek()
            self.rect = self.move_animator.goto(self.where)
        else:
            dt = pygame.time.get_ticks()
            dh = (self.boot_start+self.boot_time) - dt
            self.move_animator.goto((0,0))
            for i in range(8, self.rect.height, 8):
                pygame.draw.line(self.screen, 
                        pygame.Color("black"), 
                        (self.rect.x, self.rect.y + i), 
                        (self.rect.width + self.rect.x, self.rect.y + i), 
                        int(self.divider/5))
            self.divider = max(1, self.divider-1)
            if (dh <= 0):
                self.ready = True
