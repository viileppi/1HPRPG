# -*- coding: UTF-8 -*-     
import pygame
import random
from os import path

class Item(pygame.sprite.Sprite):
    def __init__(self, source):
        pygame.sprite.Sprite.__init__(self)
        self.source = source
        self.screen = self.source.screen
        gun = pygame.image.load(path.join("images", "gun.png")).convert_alpha()
        run = pygame.image.load(path.join("images", "run.png")).convert_alpha()
        blast = pygame.image.load(path.join("images", "blast.png")).convert_alpha()
        self.hk_list = [run, blast, gun]
        self.kindof = random.randint(0,len(self.hk_list)-1)
        self.image = self.hk_list[self.kindof]
        self.rect = self.image.get_rect()
        self.rect.x = self.source.rect.x
        self.rect.y = self.source.rect.y
        self.items = {  "speed": self.source.player.speed,
                        "blast_radius": self.source.player.blast_radius,
                        "shots_n": self.source.player.spawner.shots_n
                    }

    def destroy(self):
        self.kill()
        del self

    def update(self):
        pass
        #self.rect = self.screen.blit(
        #        self.image, 
        #        self.rect, 
        #        self.rect
        #        )

    def levelUp(self, target):
        if self.kindof == 0:
            target.speed += 2
            self.items["speed"] = target.speed
        if self.kindof == 1:
            target.blast_radius += 32
            self.items["blast_radius"] = target.blast_radius
        if self.kindof == 2:
            target.spawner.shots_n += 1
            self.items["shots_n"] = target.spawner.shots_n
        return self.items
