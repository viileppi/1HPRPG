# -*- coding: UTF-8 -*-     
import pygame
from animator import Animator

class Corpse(pygame.sprite.Sprite):
    """ generic class for everything """
    def __init__(self, source):
        """ image should be a spritesheet of square sprites """
        pygame.sprite.Sprite.__init__(self)
        self.source = source
        self.image = pygame.image.load(self.source.death_image).convert_alpha()
        #self.rect = Rect(coords[0], coords[1], self.image.get_height(), self.image.get_height())
        self.rect = source.rect
        self.screen = self.source.screen
        self.death_animator = Animator(self.screen, self.image, self.rect)
        self.countdown = self.death_animator.frame_count
        self.dir = (0,0)
        self.alive = True
        self.facing_right = True

    def update(self):
        if (self.countdown > 0):
            self.death_animator.move = (self.death_animator.move+1)%self.death_animator.frame_count
            self.death_animator.goto(self.dir)
            self.countdown -= 1
            self.draw()
        else:
            self.kill()

    def draw(self):
        self.rect = self.screen.blit(
                self.image, 
                self.rect, 
                self.rect
                )


