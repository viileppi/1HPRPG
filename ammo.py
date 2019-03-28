# -*- coding: UTF-8 -*- 
import pygame
from pygame.locals import *
from pygame.math import Vector2
import objects

class Ammo(objects.Object):
    
    def __init__(self, screen, image, coords, direction, speed):
        objects.Object.__init__(self, screen, image, coords, 1)
        self.speed = speed
        self.length = 1000
        self.start = pygame.time.get_ticks()
        self.image.fill(Color("yellow"))
        # self.dir = (direction[0] * self.speed, direction[1] * self.speed)
        self.dir = direction

    def make_shot(self, d):
        return lambda d : Ammo(self.screen, self.ammo_image, (self.rect[0], self.rect[1]), d)


    def update(self):
        if ((pygame.time.get_ticks() - self.start) < self.length):
            self.rect = self.move_animator.goto(self.dir)
            r = self.screen.blit(
                    self.image, 
                    self.rect, 
                    self.rect
                    )
        else:
            self.dir = (0,0)
            self.destroy()

class deltaAmmo(Ammo):
    """ interpolates to given coordinate by given speed """
    def __init__(self, screen, image, coords, direction, speed):
        Ammo.__init__(self, screen, image, coords, direction, speed)
        # overrides for testing
        self.length = 2000
        self.speed = 4
        # from
        # self.v1 = Vector2(self.get_pos())
        self.v1 = Vector2(coords)
        # to
        self.v2 = Vector2(direction)
        # target vector
        self.v3 = self.v2 - self.v1
        # calculate speed
        self.v4 = self.v3.normalize()
        self.v4 = self.v4 * self.speed

    def update(self):
        # destroy ammo if it's been alive for longer than self.length
        if ((pygame.time.get_ticks() - self.start) < self.length):
            # doesn't use animator for movement
            self.rect.move_ip(self.v4)
            r = self.screen.blit(
                    self.image, 
                    self.rect, 
                    self.rect
                    )
        else:
            self.dir = (0,0)
            self.destroy()

class Blast(pygame.sprite.Sprite):
    """ short-range ammo in all directions """
    def __init__(self, screen, source, radius):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.source = source
        self.radius = radius
        self.deltaR = 2
        self.speed = 4
        self.color = pygame.Color("red")
        self.rect = pygame.draw.circle(self.screen, self.color, self.source.get_pos(), self.deltaR, 2)
        self.image = pygame.Surface((self.rect.width, self.rect.height))

    def update(self):
        self.deltaR += self.speed
        if (self.deltaR < self.radius):
            self.rect = pygame.draw.circle(self.screen, self.color, self.source.get_pos(), self.deltaR, 2)
        else:
            self.destroy()

    def draw(self):
        self.rect = self.screen.blit(
                self.image, 
                self.rect, 
                self.rect
                )

    def destroy(self):
        self.kill()
        del self


