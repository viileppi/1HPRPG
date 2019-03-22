# -*- coding: UTF-8 -*-     
import maptest
import os

class LevelManager:
    """ manages operations such as switching to next level """
    def __init__(self, screen):
        self.levels = []
        l = os.listdir("levels")
        l.sort()
        for t in l:
            if (t.split(".")[1] == "tmx"):
                self.levels.append(os.path.join("levels", t))
                print(t)
        self.total_levels = len(self.levels)
        self.index = 0
        self.screen = screen
        self.current_level = maptest.TiledRenderer(self.screen, self.levels[self.index])
        print(self.levels[self.index])
        self.index = (self.index + 1) % self.total_levels

    def next(self):
        print(self.levels[self.index])
        # del self.current_level
        self.current_level = maptest.TiledRenderer(self.screen, self.levels[self.index])
        self.index = (self.index + 1) % self.total_levels
        return self.current_level

