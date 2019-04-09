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
    def __init__(self, source, radius):
        pygame.sprite.Sprite.__init__(self)
        self.source = source
        self.screen = self.source.screen
        self.radius = radius
        self.deltaR = 2
        self.speed = 2
        self.blast_w = 2
        self.color = pygame.Color("red")
        self.rect = pygame.draw.circle(self.screen, self.color, self.source.get_pos(), self.deltaR, self.blast_w)
        self.image = pygame.Surface((self.rect.width, self.rect.height))

    def update(self):
        self.deltaR += int(self.radius/(self.deltaR*2)+1)
        if (self.deltaR < self.radius):
            self.rect = pygame.draw.circle(self.screen, self.color, self.source.get_pos(), self.deltaR, self.blast_w)
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


