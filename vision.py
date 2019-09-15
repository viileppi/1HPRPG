
import pygame
from pygame.locals import *
from hud import HUD
from hud import HotKeys
from os import path
import xml.etree.ElementTree as ET

tree = ET.parse("settings.xml")
root = tree.getroot().find("vision")
# resolutionx = int(root.find("resolutionx").text)

class Screen:
    """ screen handling top class """
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.top_h = int(root.find("top_h").text)
        self.bottom_h = int(root.find("bottom_h").text)
        self.middle_h = self.height - self.top_h - self.bottom_h
        if (root.find("fullscreen").text == "True"):
            #self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.screen.set_colorkey(SRCALPHA)
        #self.gamearea = pygame.Rect(0, self.margin, self.width, (self.height - self.margin * 2))
        self.gamearea = self.screen.subsurface(Rect(0, self.top_h, self.width, self.middle_h)) 
        self.area_rect = self.gamearea.get_rect()
        ## using semi-transparent image for clearing the screen and smoothing out animation
        # self.bg = pygame.image.load(path.join("images", "alpha_fill.png")).convert_alpha()
        self.bg = pygame.Surface((self.gamearea.get_width(), self.gamearea.get_height()))
        self.bg.fill(pygame.Color("black"))
        self.top_msg = HUD((8,0), self.top_h, Color("yellow"), "Score: 0")
        gun = pygame.image.load(path.join("images", "gun.png")).convert_alpha()
        run = pygame.image.load(path.join("images", "run.png")).convert_alpha()
        blast = pygame.image.load(path.join("images", "blast.png")).convert_alpha()
        self.hk_list = [run, blast, gun]
        #self.bottom_msg = HotKeys((self.width, self.bottom_h), 16, self.hk_list)
        self.line_w = 1

    def update(self):
        self.top_msg.update()
        self.screen.blit(self.top_msg.background, (0,0))
        self.screen.blit(self.top_msg.image, (0,0))
        #self.screen.blit(self.bottom_msg.image, (self.bottom_h, self.height - self.bottom_h))
        #self.screen.blit(self.bg, (0,self.top_h))
        self.gamearea.blit(self.bg, self.area_rect, self.area_rect)

    def update_menu(self):
        pass

    def load_animation(self):
        if (self.line_w < 30):
            for y in range(0, self.height, 30):
                pygame.draw.line(self.screen, pygame.Color("black"), (0,y), (self.width,y), self.line_w)
            self.line_w += 1
            return True
        else:
            return False 
