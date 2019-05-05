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
        self.bg_color = pygame.Color("black")
        self.message = font.Font(None, size)
        self.image = self.message.render(self.text, False, self.color, self.bg_color)
        self.rect = self.image.get_rect()
        self.background = pygame.Surface((self.rect[0], self.rect[1]))
        self.background.fill(pygame.Color("blue"))

    def update(self):
        pass


    def set_message(self, string):
        self.text = string
        self.image.blit(self.background, self.rect)
        self.image = self.message.render(self.text, False, self.color, self.bg_color)

class HotKeys:
    def __init__(self, size, spacing, l):
        pygame.font.init()
        self.text = ""
        self.color = pygame.Color("grey")
        self.bg_color = pygame.Color("black")
        self.message = font.Font(None, spacing*3)
        self.image = pygame.Surface((size[0], size[1]))
        self.rect = self.image.get_rect()
        self.background = pygame.Surface((self.rect[0], self.rect[1]))
        self.background.fill(pygame.Color("blue"))
        self.icons = l
        self.spacing = spacing
        self.pos = 0
        self.busy = []
        for item in self.icons:
            self.busy.append(item.copy())
        #for icon in self.icons:
        #    self.image.blit(icon, (self.pos, 0))
        #    self.pos += icon.get_width() + self.spacing
        self.update([0,0,0])

    def update(self, l):
        self.pos = 0
        i = 0
        for icon in self.icons:
            self.image.blit(icon, (self.pos, 0))
            self.pos += icon.get_width() + self.spacing
            nro = self.message.render(str(l[i]), False, self.color, self.bg_color)
            self.image.blit(nro, (self.pos, 0))
            self.pos += nro.get_width() + self.spacing
            i += 1

    #def setBusy(self, item):
    #    self.pos = 0
    #    self.icons[item].fill(pygame.Color("black"))
    #    for icon in self.icons:
    #        self.image.blit(icon, (self.pos, 0))
    #        self.pos += icon.get_width() + self.spacing


    #def setAvailable(self, item):
    #    self.pos = 0
    #    self.icons[item] = self.busy[item].copy()
    #    for icon in self.icons:
    #        self.image.blit(icon, (self.pos, 0))
    #        self.pos += icon.get_width() + self.spacing


