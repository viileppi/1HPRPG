# -*- coding: UTF-8 -*-     
import pygame
from pygame.locals import *
from animator import Animator
import random
class ActionTile(pygame.sprite.Sprite):
    """ generic class for everything """
    def __init__(self, screen, image, coords, size):
        """ image should be a spritesheet of square sprites """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = Rect(coords[0], coords[1], self.image.get_width(), self.image.get_height())
        self.screen = screen
        self.mask = pygame.mask.from_surface(self.image)
        self.dir = (0,0)
        # self.group = group
        # self.group.add(self.move_animator)

    def destroy(self):
        self.kill()
        del self

    def move(self, coords):
        self.dir = coords

    def draw(self):
        r = self.screen.blit(
                self.image, 
                self.rect, 
                self.rect
                )
    def turnaround(self, point):
        self.dir = (self.dir[0] * -1,self.dir[1] * -1)
        self.update()

    def update(self):
        self.draw()


