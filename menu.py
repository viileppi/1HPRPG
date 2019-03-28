import vision
import pygame
from pygame import font
from pygame import color
from pygame.locals import *

class Menu(vision.Screen):
    """ menu sub-screen """
    def __init__(self, screen):
        self.width = screen.get_width()
        self.height = screen.get_height()
        vision.Screen.__init__(self, self.width, self.height)
        font.init()
        self.fontsize = 64
        self.color = color.Color("yellow")
        self.chosen = color.Color("green")
        self.message = font.Font(None, self.fontsize)
        self.pos = (64,64)
        self.menuitems = {
                            "quit": 0,
                            "continue": 1,
                            "next level": 2
                         }
        self.index = 0

    def menuloop(self):
        running = True
        while running:
            y_offset = 0
            for i, k in enumerate(self.menuitems):
                v = self.menuitems[k]
                if (v == self.index):
                    txt = self.message.render(k, False, self.chosen)
                else:
                    txt = self.message.render(k, False, self.color)
                r = self.screen.blit(
                    txt, 
                    (self.pos[0], self.pos[1] + y_offset), 
                    )
                y_offset += self.fontsize
            EventList = pygame.event.get() 
            for e in EventList:
                if (e.type == KEYDOWN):
                    k = pygame.key.get_pressed()
                    if (k[K_ESCAPE]):
                        running = False
                    if (k[K_UP]):
                        self.index = (self.index - 1) % len(self.menuitems)
                    if (k[K_DOWN]):
                        self.index = (self.index + 1) % len(self.menuitems)
                    if (k[K_RETURN]):
                        if (self.index == 0):
                            running = False
                            return 0
                        if (self.index == 1):
                            self.running = False
                            return 1
                        if (self.index == 2):
                            return 2


            self.update()
            pygame.display.update()

         

