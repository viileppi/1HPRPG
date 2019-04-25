import vision
import pygame
from pygame import font
from pygame import color
from pygame.locals import *
import keymap
import xml.etree.ElementTree as ET
from readkeys import KeyReader

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
        self.fontsize = int(self.height/15)
        self.color = color.Color("brown")
        self.chosen = color.Color("pink")
        self.message = font.Font(None, self.fontsize)
        self.pos = (self.fontsize,self.fontsize)
        self.keyreader = KeyReader()
        self.menuitems = [
                            "continue",
                            "quit",
                            "Choose keymap"
                         ]
        self.index = 0
        self.has_joystick = False
        pygame.joystick.init()
        if (pygame.joystick.get_count() > 0):
            self.joypad = pygame.joystick.Joystick(0)
            self.joypad.init()
            self.has_joystick = True

    def menuloop(self):
        running = True
        start = False
        b_button = False
        while running:
            # render menu
            y_offset = 0
            for i in range(len(self.menuitems)):
                if (i == self.index):
                    txt = self.message.render(self.menuitems[i], False, self.chosen)
                else:
                    txt = self.message.render(self.menuitems[i], False, self.color)
                r = self.screen.blit(
                    txt, 
                    (self.pos[0], self.pos[1] + y_offset), 
                    )
                y_offset += self.fontsize

            # evaluate keypresses
            EventList = pygame.event.get() 
            for e in EventList:
                if (e.type == JOYAXISMOTION):
                    self.index = int(self.index + self.joypad.get_axis(1)) % len(self.menuitems)
                if (e.type == JOYBUTTONDOWN):
                    start = self.joypad.get_button(11) == 1
                    b_button = self.joypad.get_button(1) == 1
                if (e.type == KEYDOWN):
                    k = pygame.key.get_pressed()
                    keys = self.keyreader.readKeyDwn(k)
                    self.index = (self.index + keys[0][1]) % len(self.menuitems)
                    #self.tab = (self.tab + keys[0][0]) % len(self.tabs)
                    action = keys[1]

                    if (action == "menu"):
                        running = False
                    if (action == "fire") or (action == "choose"):
                        running = False
                        return self.menuitems[self.index]

            self.update_menu()
            pygame.display.update()

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
                    self.update_menu()
                    pygame.display.update()
                    self.index += 1
                    pygame.time.wait(500)
                    self.screen.fill(Color("black"))
                if (self.index == len(self.menuitems)):
                    running = False
                    self.screen.fill(Color("black"))
            self.update_menu()
            pygame.display.update()
        for keycode in self.root.iter("key"):
            keycode.find("value").text = str(ret[keycode.get("name")])
        self.tree.write("keymap.xml")
        return ret



