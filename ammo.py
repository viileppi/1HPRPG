# -*- coding: UTF-8 -*- 
import pygame
from pygame.locals import *
from pygame.math import Vector2
import objects

class Ammo(objects.Object):
    
    def __init__(self, source, image, coords, direction, speed):
        objects.Object.__init__(self, source, image, coords)
        self.source = source
        self.speed = speed
        self.length = 2000
        self.start = pygame.time.get_ticks()
        self.image.fill(Color("yellow"))
        # self.dir = (direction[0] * self.speed, direction[1] * self.speed)
        self.dir = direction

    def make_shot(self, d):
        return lambda d : Ammo(self.screen, self.ammo_image, (self.rect[0], self.rect[1]), d)


    def update(self):
        if ((pygame.time.get_ticks() - self.start) < self.length):
            self.rect = self.move_animator.goto(self.dir)
            r = self.screen.blit(
                    self.image, 
                    self.rect, 
                    self.rect
                    )
        else:
            self.dir = (0,0)
            self.destroy()

class Spawner:
    def __init__(self, source, spawnable, cooldown, speed, image, shots_n, group):
        self.source = source
        self.spawnable = spawnable
        self.cooldown = cooldown
        self.shoot_start = pygame.time.get_ticks() - self.cooldown
        self.ammo_image = image
        self.ammo_speed = speed
        self.shots_n = shots_n
        self.shot_list = []
        self.screen = self.source.screen
        self.ammogroup = group

    def cast(self, direction):
        r = False
        where = direction
        pos = (self.source.rect.centerx - self.source.old_dir[0] * -5, self.source.rect.centery - self.source.old_dir[1] * -5)
        if (((pygame.time.get_ticks() - self.shoot_start) > self.cooldown)):
            if (len(self.ammogroup.sprites()) < self.shots_n):
                pew = self.spawnable(self, self.ammo_image, pos, where, self.ammo_speed)
                self.ammogroup.add(pew)
                self.shot_list.append(pew)
                self.shoot_start = pygame.time.get_ticks()
                r = True
        return r

class deltaAmmo(Ammo):
    """ interpolates to given coordinate by given speed """
    def __init__(self, source, image, coords, direction, speed):
        Ammo.__init__(self, source, image, coords, direction, speed)
        # overrides for testing
        #self.length = 4000
        self.speed = speed
        # from
        # self.v1 = Vector2(self.get_pos())
        self.v1 = Vector2(coords)
        # to
        self.v2 = Vector2(direction)
        # target vector
        self.v3 = self.v2 - self.v1
        # calculate speed
        self.v4 = self.v3.normalize()
        self.v4 = self.v4 * self.speed
        self.screen_w = self.screen.get_width()
        self.screen_h = self.screen.get_height()

    def destroy(self):
        self.kill()
        del self


    def update(self):
        # destroy ammo if it goes off the screen
        if (
                (self.rect.x < 0) or (self.rect.x > self.screen_w) or
                (self.rect.y < 0) or (self.rect.y > self.screen_h)
                ):
            self.dir = (0,0)
            self.destroy()
            # doesn't use animator for movement
        else:
            self.rect.move_ip(self.v4)
            r = self.screen.blit(
                    self.image, 
                    self.rect, 
                    self.rect
                    )

class Blast(pygame.sprite.Sprite):
    """ short-range ammo in all directions """
    #def __init__(self, source, image, coords, direction, speed):
    def __init__(self, source, image, coords, direction, speed):
        pygame.sprite.Sprite.__init__(self)
        self.source = source
        self.screen = self.source.screen
        self.radius = 64
        self.coords = (int(coords[0]), int(coords[1]))
        self.deltaR = 2
        self.speed = int(speed)
        self.blast_w = 2
        self.color = pygame.Color("red")
        #self.rect = pygame.draw.circle(self.screen, self.color, self.coords, self.deltaR, self.blast_w)
        self.rect = pygame.draw.circle(self.screen, self.color, self.source.source.get_pos(), self.deltaR, self.blast_w)
        self.image = pygame.Surface((self.rect.width, self.rect.height))

    def update(self):
        self.deltaR += int(self.radius/(self.deltaR*2)+1)
        if (self.deltaR < self.radius):
            self.rect = pygame.draw.circle(self.screen, self.color, self.source.source.get_pos(), self.deltaR, self.blast_w)
        else:
            self.destroy()

    def draw(self):
        self.rect = self.screen.blit(
                self.image, 
                self.rect, 
                self.rect
                )

    def destroy(self):
        self.kill()
        del self

class Bomb(Blast):
    #def __init__(self, source, image, coords, direction, speed):
    #    Blast.__init__(self, source, image, coords, direction, speed)

    def update(self):
        # self.speed is the delay of timer
        if (self.speed > 0):
            self.speed -= 1
            blink = (self.speed*8)%255
            self.image = pygame.draw.rect(self.screen, 
                    pygame.Color(blink, blink, blink), 
                    pygame.Rect(self.coords[0], 
                        self.coords[1],
                        16,
                        16))
        else:
            self.deltaR += int(self.radius/(self.deltaR*2)+2)
            if (self.deltaR < self.radius):
                self.rect = pygame.draw.circle(self.screen, self.color, self.coords, self.deltaR, self.blast_w)
                self.blast_w = self.deltaR
            else:
                self.destroy()


