import vision
import time
import readkeys as keyreader
import pickle
import pygame

class Hiscore:
    ''' class to display and enter hiscores '''
    def __init__(self, screen):
        self.screen = screen
        self.rect = screen.get_rect()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.scoreboard = pickle.load( open( "scores.pickle", "rb" ) )
        self.keyreader = keyreader.KeyReader()
        self.max_n = 10
        self.fade_step = int(255/self.max_n)
        self.color = pygame.Color(255,255,255)
        pygame.font.init()
        self.fontsize = int(self.height/15)
        self.message = pygame.font.Font(None, self.fontsize)        
        self.pos = (self.fontsize,self.fontsize)        

    def get_score(self):
        return self.scoreboard

    def draw(self):
        self.screen.fill(pygame.Color("black"))
        for i, entry in enumerate(self.scoreboard):
            text = str(entry[0]) + " " + str(entry[1])
            shade = self.fade_step * i
            colour = int(255 - shade)
            surf = self.message.render(text, False, pygame.Color(colour, colour, 0), None)
            self.screen.blit(surf, (self.pos[0], self.pos[1]+(i*self.fontsize)))
        pygame.display.update()

    def add(self, name, score):
        for i, entry in enumerate(self.scoreboard):
            if entry[0] < score:
                self.scoreboard.insert(i, [name, score])
        if (len(self.scoreboard) > self.max_n):
            self.scoreboard.pop()
        pickle.dump( self.scoreboard, open("scores.pickle", "wb") )

