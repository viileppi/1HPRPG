# -*- coding: UTF-8 -*-     
import pygame
from pygame import font

class HUD:
    """ class for displaying information on screen """
    def __init__(self, pos, size, color, text):
        self.pos = pos
        pygame.font.init()
        self.text = text
        self.color = color
        self.message = font.Font(None, size)
        self.image = self.message.render(self.text, False, self.color)
        self.rect = self.image.get_rect()
        self.background = pygame.Surface((self.rect[0], self.rect[1]))
        self.background.fill(pygame.Color("black"))

    def update(self):
        pass


    def set_message(self, string):
        self.text = string
        self.image = self.message.render(self.text, False, self.color)

class HotKeys:
    def __init__(self, size, spacing, l):
        self.icons = l
        self.image = pygame.Surface(size)
        self.spacing = spacing
        self.image.fill(pygame.Color("black"))
        self.pos = 0
        for icon in self.icons:
            self.image.blit(icon, (self.pos, 0))
            self.pos += icon.get_width() + spacing

