# -*- coding: UTF-8 -*-     
import pygame
from pygame.locals import *
import xml.etree.ElementTree as ET

class KeyReader:
    def __init__(self):
        tree = ET.parse("keymap.xml")
        root = tree.getroot()

        self.kd = {}
        for keycode in root.findall("key"):
            value = int(keycode.find("value").text)
            name = keycode.get("name")
            self.kd[name] = value
        self.keyh = {
               self.kd["right"]: 1,
               self.kd["left"]: -1
               }
        self.keyv = {
               self.kd["up"]: -1,
               self.kd["down"]: 1
               }
        self.keya = {
               pygame.K_RETURN: "choose", 
               self.kd["fire"]: "fire", 
               self.kd["blast"]: "blast",
               self.kd["bomb"]: "bomb",
               self.kd["run"]: "run"
               }
        self.joymap = {
               1: "fire",
               0: "blast",
               4: "run"
               }
        self.last_call = pygame.time.get_ticks()
        self.machine_gun_time = 750

    def readMouse(self):
        #print(pygame.mouse.get_pressed())
        r = (0,0)
        button = pygame.mouse.get_pressed()
        if (button == (1, 0, 0)):
            r = pygame.mouse.get_pos()
        if (button == (0, 0, 1)):
            pass
        return r

    def readJoypad(self, joypad):
        keys = [(0,0), None]
        start = joypad.get_button(11)
        select = joypad.get_button(10)
        #x_button = joypad.get_button(3)
        #y_button = joypad.get_button(4)
        #a_button = joypad.get_button(0)
        #b_button = joypad.get_button(1)

        if (start * select == 1):
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        if (start):
            keys = [(0,0), "menu"]
        else:
            for bn in self.joymap.keys():
                action = self.joymap[bn]
            x_axis = joypad.get_axis(0)
            y_axis = joypad.get_axis(1)
            keys = [(x_axis, y_axis), action]
        return keys

    def readKeyDwn(self, k):
        x_axis = 0
        y_axis = 0
        action = None
        if (k[K_BACKSPACE]):
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        else:
            for key,v in self.keyh.items():
                if (k[key]):
                    x_axis = self.keyh[key]
            for key,v in self.keyv.items():
                if (k[key]):
                    y_axis = self.keyv[key]
            for key,v in self.keya.items():
                if (k[key]):
                    action = self.keya[key]
        if (k[K_ESCAPE]):
            action = "menu"        
        keys = [(x_axis,y_axis), action]
        return keys

    def readKeyUp(self, k):
        pass

