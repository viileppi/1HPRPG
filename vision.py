
import pygame
from pygame.locals import *
from hud import HUD
from hud import HotKeys
from os import path

class Screen:
    """ screen handling top class """
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.top_h = 48
        self.bottom_h = 32
        self.middle_h = self.height - self.top_h - self.bottom_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        #self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN, pygame.HWSURFACE)
        #self.screen.set_colorkey(SRCALPHA)
        #self.gamearea = pygame.Rect(0, self.margin, self.width, (self.height - self.margin * 2))
        self.gamearea = self.screen.subsurface(Rect(0, self.top_h, self.width, self.middle_h)) 
        self.area_rect = self.gamearea.get_rect()
        ## using semi-transparent image for clearing the screen and smoothing out animation
        # self.bg = pygame.image.load(path.join("images", "alpha_fill.png")).convert_alpha()
        self.bg = pygame.Surface((self.gamearea.get_width(), self.gamearea.get_height()))
        self.bg.fill(pygame.Color("black"))
        self.top_msg = HUD((8,0), self.top_h, Color("yellow"), "Level 0")
        gun = pygame.image.load(path.join("images", "gun.png")).convert_alpha()
        run = pygame.image.load(path.join("images", "run.png")).convert_alpha()
        blast = pygame.image.load(path.join("images", "blast.png")).convert_alpha()
        self.hk_list = [gun, run, blast]
        self.bottom_msg = HotKeys((self.width, self.bottom_h), 16, self.hk_list)

    def update(self):
        self.screen.blit(self.bg, (0,self.top_h))
        self.top_msg.update()
        self.screen.blit(self.top_msg.background, (0,0))
        self.screen.blit(self.top_msg.image, (0,0))
        self.screen.blit(self.bottom_msg.image, (self.bottom_h, self.height - self.bottom_h))

    def update_menu(self):
        pass


