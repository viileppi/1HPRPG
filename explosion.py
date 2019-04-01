# -*- coding: UTF-8 -*-     
import pygame

class Explosion(pygame.sprite.Sprite):
    """ short-range ammo in all directions """
    def __init__(self, screen, source, radius):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.source = source
        self.radius = radius
        self.color = pygame.Color("red")
        self.rect = pygame.draw.circle(self.screen, self.color, self.source.get_pos(), self.deltaR, self.blast_w)
        self.image = pygame.Surface((self.rect.width, self.rect.height))


