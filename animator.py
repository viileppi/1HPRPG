# -*- coding: UTF-8 -*-     
import pygame
from pygame.locals import *

class Animator:
    def __init__(self, screen, image, crop, step):
        self.screen = screen
        self.image = pygame.image.load(image).convert()
        self.step = step
        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()
        self.crop_size = self.image_h
        self.move = 0
        self.image_crop = crop
        self.crop_init = self.image_crop
        self.image_pos = (step, step)
        self.move_len = 32
        self.move_steps = self.move_len
        self.target = (0,0)
        self.facing_right = True
        self.step_multi = 4
    def move_player(self, whereto):
        
        self.target = whereto
        if (self.target[0] < 0 and self.facing_right):
            print("flip2left")
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing_right = False
        elif (self.target[0] > 0 and (not self.facing_right)):
            print("flip2right")
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing_right = True
        if (self.image_crop[2] > (self.image_w - self.crop_size)):
            self.image_crop = self.crop_init
        if (self.move_steps > 0 and whereto != (0,0)):
            self.move_steps -= 1
            if (self.target[0] != 0 or self.target[1] != 0):
                self.image_pos = (self.image_pos[0] + whereto[0], self.image_pos[1] + whereto[1])
                self.target = (
                        abs(self.target[0] - self.target[0]), 
                        abs(self.target[1] - self.target[1])
                        )
                # self.image_crop = (
                #         (self.image_crop[0] + self.crop_size), self.image_crop[1],
                #         (self.image_crop[2] + self.crop_size), 
                #         self.image_crop[3]
                #         )
            self.image_crop.move_ip(self.crop_size,0)           
            self.move += self.crop_size
            if (self.move >= self.image_w):
                self.image_crop.move_ip(self.image_w * -1, 0)
                self.move = 0
            r = self.screen.blit(self.image, self.image_pos, self.image_crop)
            return False
        else:
            return True


