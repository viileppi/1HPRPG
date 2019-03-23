
import pygame
from pygame.locals import *
from hud import HUD
from os import path

class Screen:
    """ screen handling top class """
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.screen.set_colorkey(SRCALPHA)
        ## using semi-transparent image for clearing the screen and smoothing out animation
        self.bg = pygame.image.load(path.join("images", "alpha_fill.png")).convert_alpha()
        self.top_msg = HUD((8,0), 48, Color("yellow"), "Level 0")

    def update(self):
        self.screen.blit(self.bg, (0,32))
        self.screen.blit(self.top_msg.image, (0,0))


