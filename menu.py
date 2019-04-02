import vision
import pygame
from pygame import font
from pygame import color
from pygame.locals import *
import keymap

class Menu(vision.Screen):
    """ menu sub-screen """
    def __init__(self, screen):
        try:
            self.width = screen.width
            self.height = screen.height
        except AttributeError:
            self.width = screen.get_width()
            self.height = screen.get_height()
        vision.Screen.__init__(self, self.width, self.height)
        font.init()
        self.fontsize = int(self.height/10)
        self.color = color.Color("brown")
        self.chosen = color.Color("pink")
        self.message = font.Font(None, self.fontsize)
        self.pos = (self.fontsize,self.fontsize)
        self.menuitems = {
                            "continue": 0,
                            "quit": 1,
                            "next level": 2,
                         }
        self.index = 0

    def menuloop(self):
        running = True
        while running:
            # render menu
            y_offset = 0
            for v, k in self.menuitems.items():
                if (k == self.index):
                    txt = self.message.render(v, False, self.chosen)
                else:
                    txt = self.message.render(v, False, self.color)
                r = self.screen.blit(
                    txt, 
                    (self.pos[0], self.pos[1] + y_offset), 
                    )
                y_offset += self.fontsize
            # evaluate keypresses
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
                        return self.index

            self.update_menu()
            pygame.display.update()

