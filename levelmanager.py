# -*- coding: UTF-8 -*-     
import maptest
import os
import pygame

class LevelManager:
    """ manages operations such as switching to next level """
    def __init__(self, screen, player_keymap_i):
        self.total_levels = 255
        self.index = 0
        self.screen = screen
        self.player_keymap_i = player_keymap_i
        self.xy = (123,251)
        self.current_level = maptest.LevelRenderer(self.screen, self.xy, (692, 260), self.player_keymap_i) 
        self.start_top = (self.current_level.width/2, self.current_level.third/2)
        self.start_bottom = (self.current_level.width/2, self.current_level.third*2.33)
        self.start_left = (self.current_level.fifth*0.33, self.current_level.height/2)
        self.start_right = (self.current_level.fifth*4.33, self.current_level.height/2)
        self.index = (self.index + 1) % self.total_levels
        print(self.start_right)

    def next(self, xy):
        # del self.current_level
        notfound = True
        if (xy[0] < self.screen.width/2):
            print("right")
            start = self.start_right
            self.xy = (self.xy[0] - 1, self.xy[1])
            notfound = False
        else:
            print("left")
            start = self.start_left
            self.xy = (self.xy[0] + 1, self.xy[1])
            notfound = False
        if (notfound):
            if (xy[1] < self.screen.height/2):
                print("bottom")
                start = self.start_bottom
                self.xy = (self.xy[0], self.xy[1] - 1)
            else:
                print("top")
                start = self.start_top
                self.xy = (self.xy[0], self.xy[1] + 1)
        self.current_level = maptest.LevelRenderer(self.screen, self.xy, start, self.player_keymap_i)
        self.index = (self.index + 1) % self.total_levels
        return self.current_level

