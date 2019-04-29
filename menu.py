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
        w = self.width
        self.tab_index = 0
        self.keyreader = KeyReader()
        self.chosen = pygame.Color("white")
        self.color = pygame.Color(98,98,98)
        font.init()
        self.fontsize = int(self.height/15)
        self.message = font.Font(None, self.fontsize)        
        self.pos = (self.fontsize,self.fontsize)
        self.mainmenu = Tab(self.screen, "Main", 
            [
            Choice(self.message, "Continue", w),
            Choice(self.message, "New game", w),
            Choice(self.message, "Quit", w),
            Choice(self.message, "Difficulty: ", w, ["casual, ", "medium, ", "hard"])
            ]
            )
        self.settings = Tab(self.screen, "Settings", 
            [
            Choice(self.message, "Resolution: ", w, ["320*240, ", "800*600"]), 
            Choice(self.message, "Audio: ", w, ["on, ", "off"]), 
            Adjust(self.message, "Volume: ", w, 0, 100, 70, 10)
            ]
            )
        self.help = Tab(self.screen, "Help", 
            [
            Choice(self.message, "foobar", w)
            ]
            )
        self.items = [self.mainmenu, self.settings, self.help]
        self.clk = pygame.time.Clock()

    def header_draw(self):
        #self.screen.fill(pygame.Color("black"))
        x_offset = 0
        x_active = 0
        for i in range(len(self.items)):
            if (i == self.tab_index) and (self.items[self.tab_index].index == 0):
                #txt = self.items[i].menuitems[0].draw(True, 0)
                txt = self.items[i].title
                x_active = i
            else:
                #txt = self.items[i].menuitems[0].draw(False, 0)
                txt = self.items[i].untitle
            r = self.screen.blit(
                txt, 
                (self.pos[0] + x_offset, self.pos[1]), 
                )
            x_offset += self.screen.get_width()/len(self.items)
        return x_active


    def menuloop(self):
        running = True
        while (running):
            x_mod = 0
            tab = self.items[self.tab_index]
            # evaluate keypresses
            EventList = pygame.event.get() 
            for e in EventList:
                if (e.type == KEYDOWN):
                    k = pygame.key.get_pressed()
                    keys = self.keyreader.readKeyDwn(k)
                    if (tab.index == 0):
                        self.tab_index = (self.tab_index + keys[0][0]) % len(self.items)
                    else:
                        x_mod = keys[0][0]
                    tab.index = (tab.index + keys[0][1]) % len(tab.menuitems)
                    #self.tab = (self.tab + keys[0][0]) % len(self.tabs)
                    action = keys[1]

                    if (action == "menu"):
                        running = False
                    if (action == "fire") or (action == "choose"):
                        running = False
                        r = [tab.menuitems[tab.index].text, tab.menuitems[tab.index].active_option]
                        return r
            self.screen.fill(pygame.Color("black"))
            x_active = self.header_draw()
            tab.draw(x_active, x_mod)
            self.clk.tick(12)
            pygame.display.update()

class Tab:
    """ menu sub-screen """
    def __init__(self, screen, title, menuitems):

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
        self.title = self.message.render(title, False, self.chosen, None)
        self.untitle = self.message.render(title, False, self.color, None)
        self.menuitems = menuitems
        self.index = 0
        self.has_joystick = False
        pygame.joystick.init()
        if (pygame.joystick.get_count() > 0):
            self.joypad = pygame.joystick.Joystick(0)
            self.joypad.init()
            self.has_joystick = True

    def draw(self, x_offset, x_mod):
        # render menu
        y_offset = 32
        for i in range(1, len(self.menuitems), 1):
            if (i == self.index):
                txt = self.menuitems[i].draw(True, x_mod)
            else:
                txt = self.menuitems[i].draw(False, 0)

            r = self.screen.blit(
                txt, 
                (self.pos[0] + x_offset, self.pos[1] + y_offset), 
                )

            y_offset += self.fontsize

class Choice:
    def __init__(self, renderer, text, scr_w, *choices):
        self.message = renderer
        self.text = text
        self.width = scr_w
        self.choices = [" "]
        for c in choices:
            for d in c:
                self.choices.append(d)
        self.option_c = color.Color(255,255,0)
        self.unoption_c = color.Color(127,64,0)
        self.xindex = 0
        self.active_option = self.choices[0]
        self.has_focus = False
        self.color = color.Color("brown")
        self.chosen = color.Color("pink")

    def draw(self, has_focus, x_mod):
        self.has_focus = has_focus
        self.xindex = (self.xindex + x_mod) % len(self.choices)
        self.active_option = self.choices[self.xindex]
        last_x = 0
        if (has_focus):
            txt = self.message.render(self.text, False, self.chosen)

        else:
            txt = self.message.render(self.text, False, self.color)
        ret = pygame.Surface((self.width, txt.get_height())) 
        ret.blit(txt, (0,0))
        last_x += txt.get_width()
        for c in self.choices:
            if (c == self.active_option):
                option = self.message.render(c, False, self.option_c)
            else:
                option = self.message.render(c, False, self.unoption_c)
            ret.blit(option, (last_x,0))
            last_x += option.get_width()
        return ret

class Adjust:
    def __init__(self, renderer, text, scr_w, bottom, top, default, step):
        self.message = renderer
        self.bottom = bottom
        self.top = top
        self.step = step
        self.text = text
        self.width = scr_w
        self.xindex = default
        self.has_focus = False
        self.color = color.Color("brown")
        self.chosen = color.Color("pink")
        self.option_c = color.Color(255,255,0)
        self.unoption_c = color.Color(127,64,0)
     
    def draw(self, has_focus, x_mod):
        self.has_focus = has_focus
        xindex = self.xindex + (x_mod * self.step) 
        xindex = min(self.top, xindex)
        self.xindex = max(self.bottom, xindex)
        if (has_focus):
            txt = self.message.render(self.text, False, self.chosen)
            option = self.message.render(str(self.xindex), False, self.option_c)
        else:
            txt = self.message.render(self.text, False, self.color)
            option = self.message.render(str(self.xindex), False, self.unoption_c)
        ret = pygame.Surface((self.width, txt.get_height())) 
        ret.blit(txt, (0,0))
        last_x = txt.get_width()
        ret.blit(option, (last_x,0))
        return ret


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
        self.tree = tree
        self.root = root
        self.index = 0

    def menuloop(self):
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



