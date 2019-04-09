# -*- coding: UTF-8 -*-     
import objects
import pygame
from ammo import Ammo
from ammo import deltaAmmo
from ammo import Blast
from los import LOS
from los import Cast
from os import path
from pygame.math import Vector2
import random
import userevents
import xml.etree.ElementTree as ET

class Enemy(objects.Object):
    def __init__(self, source, image, coords, difficulty):
        """ image should be a spritesheet of square sprites """
        objects.Object.__init__(self, source, image, coords)
        self.difficulty = min(12, max(2, difficulty))
        tree = ET.parse("settings.xml")
        root = tree.getroot().find("enemy")
        fps = int(tree.getroot().find("main").find("fps").text)
        self.speed = int(root.find("speed").text) * (fps/100) * self.difficulty
        self.ammo_speed = int(root.find("ammo_speed").text) * (self.speed/2)
        self.walk_dist = int(root.find("walk_dist").text)
        self.boot_time = int(root.find("boot_time").text)
        self.cooldown = int(root.find("cooldown").text) / self.difficulty
        self.cooldown = max(100, self.cooldown)
        # self.speed = 2
        # self.walk_dist = 100
        # self.ammo_speed = 3
        # self.boot_time = 1000
        # self.cooldown = 500
        self.forward = True
        self.walked = 0
        self.where = (self.speed,0)
        self.player = self.source.player
        self.enemy_walls = self.source.enemy_walls
        self.wallgroup = self.enemy_walls
        self.enemyammo = self.source.enemyammo
        self.ray_shrink = (-24,-8)
        self.wall_list = []
        for w in self.wallgroup.sprites():
            self.wall_list.append(w.rect)
        self.ammo_image = path.join("images", "ammo.png")
        self.ammogroup = self.source.enemyammo
        self.los = LOS(self)
        self.seen_player = False
        self.ready = False
        self.shoot_start = pygame.time.get_ticks()
        self.boot_start = pygame.time.get_ticks()
        self.image_backup = self.image.copy()
        self.divider = self.rect.height
        self.cast = Cast(self)
        self.turns = [
                        (-self.speed,0), 
                        (0,-self.speed), 
                        (self.speed,0),
                        (0,self.speed), 
                        ]
        self.dir_div = 0

    def destroy(self):
        if (random.randint(0, 5) > 3):
            e = Snake(self, path.join("images", "snake.png"), (self.rect[0],self.rect[1]), self.difficulty)
            self.groups()[0].add(e)
        self.dir = (0,0)
        self.alive = False
        self.kill()
        del self
        pygame.event.post(userevents.death_event())



    def playerCheck(self, dist):
        if (self.rect.colliderect(self.player.rect.inflate(dist,dist))):
            return True
        else:
            return False

    def seek(self):
        if (self.seen_player):
            #self.where = (0,0)
            self.rect = self.move_animator.goto((0,0))
            p = self.player.get_pos()
            e = self.get_pos()
            # v1 = Vector2(p)
            # v2 = Vector2(e)
            # v3 = v1 - v2
            # print(v3.normalize())
            if (((pygame.time.get_ticks() - self.shoot_start) > self.cooldown)):
                    pew = deltaAmmo(self, self.ammo_image, e, p, self.ammo_speed)
                    self.ammogroup.add(pew)
                    self.shoot_start = pygame.time.get_ticks()
                    pygame.event.post(userevents.enemy_shot_event())
        else:
            c = self.cast.test(self.where)
            self.where = (self.where[0] * c[0], self.where[1] * c[1])
            self.rect = self.move_animator.goto(self.where)
            if (c[0] == 0) or (c[1] == 0):
                self.dir_div += 1
                self.where = self.turns[self.dir_div%len(self.turns)]

    def turnaround(self, point):
        # self.forward = not self.forward
        # self.walked = 1
        #if (self.where == (1,0)):
        #    self.where = (0,1)
        #elif (self.where == (0,1)):
        #    self.where = (-1,0)
        #elif (self.where == (0,-1)):
        #    self.where = (1,0)
        #elif (self.where == (-1,0)):
        #    self.where = (0,-1)
        #elif (self.where == (0,0)):
        #    self.where = (1,0)
        #self.move((self.where[0] * self.speed, self.where[1] * self.speed))
        #self.where = (self.where[0] * self.speed, self.where[1] * self.speed)
        #c = self.cast.test(self.where)
        #self.where = (self.where[0] * c[0], self.where[1] * c[1])
        pass

    def update(self):
        if (self.alive):
            if (self.ready):
                self.seen_player = self.los.draw()
                self.seek()
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
class Snake(Enemy):
    def __init__(self, source, image, coords, difficulty):
        # snake should paralyze and not kill the player! TODOTODOTODO
        # snakes could spawn randomly from dead enemies
        Enemy.__init__(self, source, image, coords, difficulty)
        # self.speed = 2
        # self.walk_dist = 200

        self.ray_shrink = (0,-24)
        self.cast = Cast(self)
        self.where = (1,1)
        self.attack_cool = self.boot_time
        self.speed * self.speed * 2
        self.attack_start = pygame.time.get_ticks()
        self.creation_time = pygame.time.get_ticks()
        self.turns = [
                        (-self.speed,self.speed), 
                        (-self.speed,-self.speed), 
                        (self.speed,-self.speed),
                        (self.speed,self.speed), 
                        ]
        self.dir_div = 0

    def destroy(self):
        if (self.creation_time + self.boot_time) < pygame.time.get_ticks():
            self.dir = (0,0)
            self.alive = False
            self.kill()
            del self
            pygame.event.post(userevents.death_event())
        else:
            # TODO snake shouldn't die right after the spawn...
            print("snake not ready!")

    def seek(self):
        if (self.seen_player):
            self.seen_player = False
            p = self.player.get_pos()
            e = self.get_pos()
            x = p[0] - e[0] 
            y = p[1] - e[1]
            x = min(1, max(-1, x))
            y = min(1, max(-1, y))
            self.where = (x*self.speed,y*self.speed)

    def turnaround(self, p):
        pass


    def update(self):
        c = self.cast.test(self.where)
        self.where = (self.where[0] * c[0], self.where[1] * c[1])
        if (c != (1,1)):
            self.where = self.turns[self.dir_div%len(self.turns)]
            self.dir_div += 1
        self.rect = self.move_animator.goto(self.where)

        if (self.attack_start + self.attack_cool) < pygame.time.get_ticks():
            #self.where = (self.where[0]*-1, self.where[1]*-1)
            self.seen_player = self.los.draw()
            self.attack_start = pygame.time.get_ticks()
        self.seek()

