# -*- coding: UTF-8 -*-     
import pygame
from pygame.locals import *

class Animator(pygame.sprite.Sprite):
    """ Arguments: pygame.display, spritesheet to load (string), rect of single fame, speed of movement (int)"""
    def __init__(self, screen, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.group = None
        self.screen = screen
        # self.image = pygame.image.load(image).convert()
        self.image = image        
        self.step = 2
        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()
        self.crop_size = self.image_h
        self.move = 0
        # self.image_crop = Rect(0,0,self.crop_size,self.crop_size)
        self.rect = Rect(0,0,self.crop_size,self.crop_size)
        self.crop_init = self.rect
        self.image_pos = pos
        self.target = (0,0)
        self.facing_right = True
        self.step_multi = 0
        self.doblit = True

    def add2group(self, group):
        self.group = group

    def reset(self):
        self.move = 0

    def goto(self, whereto):
        # flip image if needed
        self.target = whereto
        if (self.target[0] < 0 and self.facing_right):
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing_right = False
        elif (self.target[0] > 0 and (not self.facing_right)):
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing_right = True
        # move image smoothly
        if (whereto != (0,0)):
            self.image_pos = (self.image_pos[0] + whereto[0] * self.step, self.image_pos[1] + whereto[1] * self.step)
            self.target = (
                abs(self.target[0] - self.target[0]), 
                abs(self.target[1] - self.target[1])
                )
            # move spritesheet in place to RIGHT
            if (self.facing_right):
                self.rect.move_ip(self.crop_size,0)           
                self.move += self.crop_size
                if (self.move >= (self.image_w)):
                    self.rect.move_ip(self.image_w * -1, 0)
                    self.move = 0
                    self.rect = self.crop_init
            # move spritesheet in place to LEFT
            if (not self.facing_right):
                if (self.move <= self.crop_size):
                    self.rect.move_ip(self.image_w - self.crop_size, 0)
                    self.move = self.image_w
                    self.rect = self.crop_init
                self.rect.move_ip(-self.crop_size,0)           
                self.move -= self.crop_size
        
        if (self.doblit):
            r = self.screen.blit(
                    self.image, 
                    self.image_pos, 
                    self.rect
                    )
        else:
            r = self.rect
        return r

