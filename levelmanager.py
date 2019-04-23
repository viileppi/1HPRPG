# -*- coding: UTF-8 -*-     
import maptest
import os
import pygame
import xml.etree.ElementTree as ET
from copy import deepcopy

tree = ET.parse("settings.xml")
root = tree.getroot().find("levelmanager")
# resolutionx = int(root.find("resolutionx").text)

class LevelManager:
    """ manages operations such as switching to next level """
    def __init__(self, screen):
        self.difficulty = 1
        self.total_levels = int(root.find("total_levels").text)
        self.screen = screen
        self.player_start = (int(root.find("player_startx").text),int(root.find("player_starty").text))
        self.xy = (int(root.find("start_x").text),int(root.find("start_y").text))
        self.origin = self.xy
        self.current_level = maptest.LevelRenderer(self.screen, self.xy, self.player_start, self.difficulty) 
        self.start_top = (self.current_level.width/2, self.current_level.third/2)
        self.start_bottom = (self.current_level.width/2, self.current_level.third*2.33)
        self.start_left = (self.current_level.fifth*0.33, self.current_level.height/2)
        self.start_right = (self.current_level.fifth*4.33, self.current_level.height/2)

    def bars(self):
        while(self.screen.load_animation()):
            pygame.display.update()
            pygame.time.wait(20)

    def again(self):
        player_items = self.current_level.player_items
        self.current_level = maptest.LevelRenderer(self.screen, self.xy, self.player_start, self.difficulty)
        self.current_level.player.set_items(player_items)
        return self.current_level

    def next(self, score):
        # del self.current_level
        self.difficulty = max(1, int(score/1000))
        notfound = True
        xy = self.current_level.player.get_pos()
        player_items = self.current_level.player_items
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
        self.player_start = start
        self.current_level = maptest.LevelRenderer(self.screen, self.xy, start, self.difficulty)
        self.current_level.player.set_items(player_items)
        self.bars()
        return self.current_level

