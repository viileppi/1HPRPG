# -*- coding: UTF-8 -*-     
import pygame
from pygame.locals import *
from animator import Animator
import random
class Object:
    """ generic class for everything """
    def __init__(self, screen, image, coords, group):
        """ image should be a spritesheet of square sprites """
        self.image = pygame.image.load(image).convert_alpha()
        self.image_pos = coords
        self.screen = screen
        self.move_animator = Animator(self.screen, self.image, self.image_pos)
        self.group = group
        self.group.add(self.move_animator)
        self.forward = True
        self.walked = 0

    def collboll(self, a, b):
        print(a, b)
        return "foo"
    def move(self, coords):
        self.move_animator.goto(coords)

    def patrol(self):
        if (self.forward):
            self.move_animator.goto((1, 0))
            self.walked += 1
        if (self.walked > 50):
            self.forward = False
        if ((not self.forward)):
            self.move_animator.goto((-1, 0))
            self.walked -= 1
        if (self.walked < 0):
            self.forward = True


