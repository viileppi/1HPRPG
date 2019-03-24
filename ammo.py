# -*- coding: UTF-8 -*- 
import pygame
from pygame.locals import *
import objects

class Ammo(objects.Object):
    
    def __init__(self, screen, image, coords, direction, speed):
        objects.Object.__init__(self, screen, image, coords, 1)
        self.speed = speed
        self.length = 500
        self.start = pygame.time.get_ticks()
        self.image.fill(Color("yellow"))
        self.dir = (direction[0] * self.speed, direction[1] * self.speed)

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
