import vision
import time
import readkeys as keyreader
import pickle
import pygame
from pygame.locals import *

class Hiscore:
    ''' class to display and enter hiscores '''
    def __init__(self, screen):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.keyreader = keyreader.KeyReader()
        self.max_n = 10
        self.color = pygame.Color(255,255,255)
        pygame.font.init()
        self.fontsize = int(self.height/15)
        self.message = pygame.font.Font(None, self.fontsize)        
        self.pos = (self.fontsize,self.fontsize)        
        self.scoreboard = pickle.load( open("scoreboard.pickle", "rb"))
        self.sorted_scores = list(self.scoreboard.values())
        self.sorted_scores.sort()
        ### this might reset scoreboard when uncommented...
        ###self.scoreboard = {
        ###                    "foo": 500,
        ###                    "bar": 450
        ###                    }

    def draw(self):
        i = 0
        self.screen.fill(pygame.Color("black"))
        text = "HIGHSCORES" 
        surf = self.message.render(text, False, self.color, None)
        self.screen.blit(surf, (self.pos[0], self.pos[1]+(i*self.fontsize)))
        for sortedscore in self.sorted_scores:
            for key, value in self.scoreboard.items():
                if (value == sortedscore):
                    i += 1
                    text = str(key) + " : " + str(value)
                    surf = self.message.render(text, False, self.color, None)
                    self.screen.blit(surf, (self.pos[0], self.pos[1]+(i*self.fontsize)))
        pygame.display.update()

    def input(self, score):
        x = 0
        y = 0
        i = 0
        character = 65
        name = ["A", "A", "A"]
        self.screen.fill(pygame.Color("black"))
        text = "Game over! Input your name for scoreboard" 
        surf = self.message.render(text, False, self.color, None)
        running = True
        #inputarea = self.screen.subsurface(pygame.Rect(200, self.fontsize, self.fontsize*4, self.fontsize))
        while running:
            self.screen.fill(pygame.Color("black"))
            self.screen.blit(surf, (self.pos[0], self.pos[1]+(i*self.fontsize)))
            j = 0
            for c in name:
                s = self.message.render(c, False, self.color, pygame.Color("black"))
                #inputarea.blit(s, (200+j,200))
                self.screen.blit(s, (200+j,200))
                j += self.fontsize
            pygame.display.update()
            EventList = pygame.event.get()
            for e in EventList:
                if (e.type == pygame.KEYDOWN):
                    keys = self.keyreader.readKeyDwn(pygame.key.get_pressed())
                    if (keys[1] == "fire"):
                        # choose
                        running = False
                    else:
                        y = keys[0][1]
                        x = (x + keys[0][0])%len(name)
                        character += y
                        name[x] = chr(character)
        userinput = str(name[0]+name[1]+name[2])
        self.scoreboard[userinput] = score
        pickle.dump( self.scoreboard, open("scoreboard.pickle", "wb") )

