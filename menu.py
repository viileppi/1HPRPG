import vision
import pygame
from pygame import font
from pygame import color
from pygame.locals import *
import keymap
import xml.etree.ElementTree as ET
from readkeys import KeyReader

#class Menu(vision.Screen):

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.rect = self.screen.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.mainmenu = Tab(self.screen)
        self.mainmenu.menuitems = ["Main", "New game", "Quit", "Difficulty"]
        self.settings = Tab(self.screen)
        self.settings.menuitems = ["Settings", "Resolution", "Audio on/off", "Volume"]
        self.help = Tab(self.screen)
        self.help.menuitems = ["Help", "foobar"]
        self.items = [self.mainmenu, self.settings, self.help]
        self.tab_index = 0
        self.keyreader = KeyReader()
        self.chosen = pygame.Color("white")
        self.color = pygame.Color(98,98,98)
        font.init()
        self.fontsize = int(self.height/15)
        self.message = font.Font(None, self.fontsize)        
        self.pos = (self.fontsize,self.fontsize)

    def header_draw(self):
        #self.screen.fill(pygame.Color("black"))
        x_offset = 0
        x_active = 0
        for i in range(len(self.items)):
            if (i == self.tab_index) and (self.items[self.tab_index].index == 0):
                txt = self.message.render(self.items[i].menuitems[0], False, self.chosen)
                x_active = i
            else:
                txt = self.message.render(self.items[i].menuitems[0], False, self.color)
            r = self.screen.blit(
                txt, 
                (self.pos[0] + x_offset, self.pos[1]), 
                )
            x_offset += len(self.items[i].menuitems[0]) * 24
        return x_active


    def menuloop(self):
        running = True
        while (running):
            tab = self.items[self.tab_index]
            # evaluate keypresses
            EventList = pygame.event.get() 
            for e in EventList:
                if (e.type == KEYDOWN):
                    k = pygame.key.get_pressed()
                    keys = self.keyreader.readKeyDwn(k)
                    if (tab.index == 0):
                        self.tab_index = (self.tab_index + keys[0][0]) % len(self.items)
                    tab.index = (tab.index + keys[0][1]) % len(tab.menuitems)
                    #self.tab = (self.tab + keys[0][0]) % len(self.tabs)
                    action = keys[1]

                    if (action == "menu"):
                        running = False
                    if (action == "fire") or (action == "choose"):
                        running = False
                        return tab.menuitems[tab.index]
            self.screen.fill(pygame.Color("black"))
            x_active = self.header_draw()
            tab.draw(x_active)
            pygame.display.update()

class Tab:
    """ menu sub-screen """
    def __init__(self, screen):
        #try:
        #    self.width = screen.width
        #    self.height = screen.height
        #except AttributeError:
        #    self.width = screen.get_width()
        #    self.height = screen.get_height()
        #vision.Screen.__init__(self, self.width, self.height)
        self.rect = screen.get_rect()        
        self.screen = screen.subsurface(self.rect)
        self.width = self.rect.width
        self.height = self.rect.height
        font.init()
        self.fontsize = int(self.height/15)
        self.color = color.Color("brown")
        self.chosen = color.Color("pink")
        self.message = font.Font(None, self.fontsize)
        self.pos = (self.fontsize,self.fontsize)
        self.menuitems = [
                            "continue",
                            "quit",
                         ]
        self.index = 0
        self.has_joystick = False
        pygame.joystick.init()
        if (pygame.joystick.get_count() > 0):
            self.joypad = pygame.joystick.Joystick(0)
            self.joypad.init()
            self.has_joystick = True

    def draw(self, x_offset):
        # render menu
        y_offset = 32
        for i in range(1, len(self.menuitems), 1):
            if (i == self.index):
                txt = self.message.render(self.menuitems[i], False, self.chosen)
            else:
                txt = self.message.render(self.menuitems[i], False, self.color)
            r = self.screen.blit(
                txt, 
                (self.pos[0] + x_offset, self.pos[1] + y_offset), 
                )
            y_offset += self.fontsize

class KeySetup(Menu):
    def __init__(self, screen):
        Menu.__init__(self, screen)
        self.menuitems = {}
        tree = ET.parse("keymap.xml")
        root = tree.getroot()
        for keycode in root.findall("key"):
            value = int(keycode.find("value").text)
            name = keycode.get("name")
            self.menuitems[name] = value
        print(self.menuitems)
        self.tree = tree
        self.root = root

        #resolutionx = int(root.find("resolutionx").text)
        #self.menuitems = {
        #        0: "Up",
        #        1: "Down",
        #        2: "Left",
        #        3: "Right",
        #        4: "Shoot",
        #        5: "Blast",
        #        6: "Sprint"
        #                 }
        self.index = 0

    def menuloop(self):
        print("KeySetup menuloop")
        running = True
        s = "Press esc to cancel or key for: "
        ret = {}
        while running:
            y_offset = 0
            # render menu
            txt = self.message.render((s + list(self.menuitems)[self.index]), False, self.chosen)
            r = self.screen.blit(
                txt, 
                (self.pos[0], self.pos[1] + y_offset + (self.index*y_offset)), 
                )
            y_offset += self.fontsize
            # evaluate keypresses
            EventList = pygame.event.get() 
            for e in EventList:
                if (e.type == KEYDOWN):
                    k = pygame.key.get_pressed()
                    if (k[K_ESCAPE]):
                        running = False
                        self.screen.fill(Color("black"))
                        break
                #if (e.type == KEYUP):
                    # newkey = pygame.key.get_pressed()
                    newkey = e.key
                    print(newkey)
                    #ret.append(newkey)
                    ret[list(self.menuitems)[self.index]] = newkey
                    txt = self.message.render(pygame.key.name(newkey), False, self.chosen)
                    r = self.screen.blit(
                        txt, 
                        (self.pos[0], self.pos[1] + y_offset + self.index*y_offset), 
                        )
                    pygame.display.update()
                    self.index += 1
                    pygame.time.wait(500)
                    self.screen.fill(Color("black"))
                if (self.index == len(self.menuitems)):
                    running = False
                    self.screen.fill(Color("black"))
            pygame.display.update()
        for keycode in self.root.iter("key"):
            keycode.find("value").text = str(ret[keycode.get("name")])
        self.tree.write("keymap.xml")
        return ret



