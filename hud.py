# -*- coding: UTF-8 -*-     
import pygame
from pygame import font

class HUD:
    """ class for displaying information on screen """
    def __init__(self, pos, size, color, text):
        pygame.font.init()
        self.text = text
        self.color = color
        self.message = font.Font(None, size)
        self.image = self.message.render(self.text, False, self.color)
        self.rect = self.image.get_rect()

    def update(self):
        pass

    def set_message(self, string):
        self.text = string
        self.image = self.message.render(self.text, False, self.color)
        self.rect = self.image.get_rect()
