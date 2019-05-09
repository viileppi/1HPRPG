# -*- coding: UTF-8 -*-     
import pygame
from pygame.locals import *
from animator import Animator
import userevents

class Object(pygame.sprite.Sprite):
    """ generic class for everything """
    def __init__(self, source, image, coords):
        """ image should be a spritesheet of square sprites """
        pygame.sprite.Sprite.__init__(self)
        self.source = source
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = Rect(coords[0], coords[1], self.image.get_height(), self.image.get_height())
        self.screen = self.source.screen
        self.move_animator = Animator(self.screen, self.image, self.rect)
        self.m_image = self.image.subsurface(self.move_animator.crop_init)
        self.mask = pygame.mask.from_surface(self.m_image)
        self.dir = (0,0)
        self.alive = True
        self.speed = 1

    def destroy(self):
        self.dir = (0,0)
        self.alive = False
        self.kill()
        del self
        pygame.event.post(userevents.death_event())

    def move(self, coords):
        self.dir = (coords[0], coords[1])

    def draw(self):
        self.rect = self.screen.blit(
                self.image, 
                self.rect, 
                self.rect
                )

    def turnaround(self, point):
        pass
    
    def update(self):
        if (self.alive):
            self.rect = self.move_animator.goto(self.dir)
            self.mask = self.move_animator.current_mask
        else:
            self.destroy()

    def moveOnce(self, coords):
        self.rect = self.move_animator.goto(coords)

    def get_pos(self):
        x = (self.rect.centerx)
        y = (self.rect.centery)
        r = (x,y)
        return r



