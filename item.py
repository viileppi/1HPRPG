# -*- coding: UTF-8 -*-     
import pygame
import random
from os import path

class Item(pygame.sprite.Sprite):
    def __init__(self, source, pos):
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
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.items = {  "speed": self.source.player.speed,
                        "blast_radius": self.source.player.blast_radius,
                        "shots_n": self.source.player.ammo_spawner.shots_n,
                        "blasts_n": self.source.player.blast_spawner.shots_n
                    }
        self.timeout = 200

    def destroy(self):
        self.kill()
        del self

    def update(self):
        self.timeout -= 1
        if self.timeout < 0:
            self.destroy()
        #self.rect = self.screen.blit(
        #        self.image, 
        #        self.rect, 
        #        self.rect
        #        )

    def levelUp(self, target):
        if self.kindof == 0:
            target.speed *= 2
            self.items["speed"] = target.speed
        if self.kindof == 1:
            # we don't want too large blast but we want more blasts
            if (target.blast_radius < 100):
                target.blast_radius += 32
                self.items["blast_radius"] = target.blast_radius
            else:
                target.blast_spawner.shots_n += 1
                self.items["blasts_n"] = target.blast_spawner.shots_n
        if self.kindof == 2:
            target.ammo_spawner.ammo_speed += 1
            target.ammo_spawner.shots_n += 1
            self.items["shots_n"] = target.ammo_spawner.shots_n
        return self.items
