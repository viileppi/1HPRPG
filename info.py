# -*- coding: UTF-8 -*-     
import pygame

class Info:
    """ newline splits text into skippable segments """
    def __init__(self, screen, message):
        self.screen = screen.subsurface(pygame.Rect(
            int(screen.get_width()/3), 
            int(screen.get_height()/3), 
            int(screen.get_width()/2),
            int(screen.get_height()/8)))
        pygame.font.init()
        self.full_text = message.split("\n")
        self.text = self.full_text.pop(0)
        self.size = int(self.screen.get_height() * 0.75)
        self.color = pygame.Color("black")
        self.bg_color = pygame.Color("white")
        self.message = pygame.font.Font(None, self.size)
        self.image = self.message.render(self.text, False, self.color, self.bg_color)
        self.rect = self.image.get_rect()

    def draw(self):
        self.rect = self.screen.blit(self.image, self.rect)

    def __next__(self):
        self.text = self.full_text.pop(0)
        self.image = self.message.render(self.text, False, self.color, self.bg_color)
        self.rect = self.image.get_rect()
        return self.screen.blit(self.image, self.rect)


