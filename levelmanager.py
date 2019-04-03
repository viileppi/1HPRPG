# -*- coding: UTF-8 -*-     
import maptest
import os
import pygame
import xml.etree.ElementTree as ET

tree = ET.parse("settings.xml")
root = tree.getroot().find("levelmanager")
# resolutionx = int(root.find("resolutionx").text)

class LevelManager:
    """ manages operations such as switching to next level """
    def __init__(self, screen, player_keymap_i):
        self.total_levels = int(root.find("total_levels").text)
        self.screen = screen
        self.player_keymap_i = player_keymap_i
        self.player_start = (int(root.find("player_startx").text),int(root.find("player_starty").text))
        self.xy = (int(root.find("start_x").text),int(root.find("start_y").text))
        self.current_level = maptest.LevelRenderer(self.screen, self.xy, self.player_start, self.player_keymap_i) 
        self.start_top = (self.current_level.width/2, self.current_level.third/2)
        self.start_bottom = (self.current_level.width/2, self.current_level.third*2.33)
        self.start_left = (self.current_level.fifth*0.33, self.current_level.height/2)
        self.start_right = (self.current_level.fifth*4.33, self.current_level.height/2)

    def next(self, xy):
        # del self.current_level
        notfound = True
        if (xy[0] < self.screen.width/7):
            start = self.start_right
            self.xy = (self.xy[0] - 1, self.xy[1])
            notfound = False
        if (xy[0] > (self.screen.width - 64)):
            start = self.start_left
            self.xy = (self.xy[0] + 1, self.xy[1])
            notfound = False
        if (notfound):
            if (xy[1] < self.screen.height/5):
                start = self.start_bottom
                self.xy = (self.xy[0], self.xy[1] - 1)
            else:
                start = self.start_top
                self.xy = (self.xy[0], self.xy[1] + 1)
        self.current_level = maptest.LevelRenderer(self.screen, self.xy, start, self.player_keymap_i)
        return self.current_level

