# -*- coding: UTF-8 -*- 
import pygame
from pygame.locals import *
import objects

class Ammo(objects.Object):
    
    def __init__(self, screen, image, coords, direction):
        objects.Object.__init__(self, screen, image, coords)
        self.speed = 8
        self.length = 1000
        self.start = pygame.time.get_ticks()
        self.image.fill(Color("yellow"))
        self.dir = (direction[0] * self.speed, direction[1] * self.speed)
    def update(self):
        if ((pygame.time.get_ticks() - self.start) < self.length):
            self.move(self.dir)
            r = self.screen.blit(
                    self.image, 
                    self.rect, 
                    self.rect
                    )
        else:
            self.dir = (0,0)
            self.destroy()
