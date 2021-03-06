# -*- coding: UTF-8 -*-     
import pygame
from pygame.locals import *

class Animator(pygame.sprite.Sprite):
    def __init__(self, screen, image, pos):
        #pygame.sprite.Sprite.__init__(self)
        self.group = None
        self.screen = screen
        # self.image = pygame.image.load(image).convert()
        self.image = image        
        self.step = 0.75
        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()
        self.crop_size = self.image_h
        self.move = 0
        self.div = 0
        # self.image_crop = Rect(0,0,self.crop_size,self.crop_size)
        self.rect = Rect(0,0,self.crop_size,self.crop_size)
        self.crop_init = self.rect
        self.image_pos = pos
        self.target = (0,0)
        self.facing_right = True
        self.step_multi = 1
        self.doblit = False
        self.frames = []
        self.frames_flip = []
        self.mask_frames = []
        self.mask_frames_flip = []
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.image.scroll(-self.crop_size, 0)
        s.blit(self.image.copy(), (0,0))
        self.frames.append(s.copy())
        self.mask_frames.append(pygame.mask.from_surface(s))
        sf = pygame.transform.flip(s, True, False) 
        self.frames_flip.append(sf.copy())
        self.mask_frames_flip.append(pygame.mask.from_surface(sf))
        for i in range(int(self.image_w/self.crop_size)):
            s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            self.image.scroll(-self.crop_size, 0)
            s.blit(self.image.copy(), (0,0))
            self.frames.append(s.copy())
            self.mask_frames.append(pygame.mask.from_surface(s))
            sf = pygame.transform.flip(s, True, False) 
            self.frames_flip.append(sf.copy())
            self.mask_frames_flip.append(pygame.mask.from_surface(sf))
        self.frame_count = len(self.frames)
        #self.skip = 0
        #self.skip_n = 1
        self.die_count = 0
        self.current_mask = self.mask_frames[self.move]

    def add2group(self, group):
        self.group = group

    def reset(self):
        pass

    def goto(self, whereto):
        # flip image if needed
        self.target = whereto
        if (self.target[0] < 0 and self.facing_right):
            #self.image = pygame.transform.flip(self.image, True, False)
            self.facing_right = False
        elif (self.target[0] > 0 and (not self.facing_right)):
            #self.image = pygame.transform.flip(self.image, True, False)
            self.facing_right = True
        # move image smoothly
        if (whereto != (0,0)):
            self.image_pos = (self.image_pos[0] + whereto[0] * self.step, self.image_pos[1] + whereto[1] * self.step)
            self.target = (
                abs(self.target[0] - self.target[0]), 
                abs(self.target[1] - self.target[1])
                )
            self.div += 1
            if (self.div%self.step_multi)==0:
                self.move = (self.move+1)%self.frame_count
        if (self.facing_right):
            r = self.screen.blit(
                    self.frames[self.move],#.copy(), 
                    self.image_pos, 
                    self.rect
                    )
            self.current_mask = self.mask_frames[self.move]
        else:
            r = self.screen.blit(
                    self.frames_flip[self.move],#.copy(), 
                    self.image_pos, 
                    self.rect
                    )
            self.current_mask = self.mask_frames_flip[self.move]
        return r


