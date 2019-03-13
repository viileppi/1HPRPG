# -*- coding: UTF-8 -*-     
import pygame
from pygame.locals import *
from animator import Animator
import random
class Object(pygame.sprite.Sprite):
    """ generic class for everything """
    def __init__(self, screen, image, coords):
        """ image should be a spritesheet of square sprites """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = Rect(coords[0], coords[1], self.image.get_height(), self.image.get_height())
        self.screen = screen
        self.move_animator = Animator(self.screen, self.image, self.rect)
        # self.group = group
        # self.group.add(self.move_animator)
        self.forward = True
        self.walked = 0
        self.walk_dist = 100

    def destroy(self):
        self.kill()
        del self

    def collboll(self, a, b):
        print(a, b)
        return "foo"
    def move(self, coords):
        self.rect = self.move_animator.goto(coords)

    def draw(self):
        r = self.screen.blit(
                self.image, 
                self.rect, 
                self.rect
                )

    def patrol(self):
        coords = (0,0)
        if (self.forward):
            coords = (1, 0)
            self.walked += 1
        if (self.walked > self.walk_dist):
            self.forward = False
        if ((not self.forward)):
            coords = (-1, 0)
            self.walked -= 1
        if (self.walked < 0):
            self.forward = True
        self.move(coords)

    def turnaround(self):
        self.forward = not self.forward
        self.walked = 1

    def update(self):
        self.patrol()


