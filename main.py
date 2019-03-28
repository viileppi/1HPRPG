#!/usr/bin/env python3
from os import listdir
from os import path
import pygame
from pygame.locals import *
import pytmx
from pytmx.util_pygame import load_pygame
import maptest
from ammo import Ammo 
from colliders import *
import levelmanager
from vision import Screen
from menu import Menu

# init stuff
scr = Screen(800, 600)
screen = scr.screen
level = levelmanager.LevelManager(scr)
tiled_map = level.current_level

# map is rendered on background image
tiled_map.render_map(scr.bg)

# set some variables
finish = tiled_map.finish
running = True
pygame.init()

# setup framerate and keyboard repeat rate
clk = pygame.time.Clock()
fps = 60
pygame.key.set_repeat(50,50)
pygame.display.update()

while running:
    # uncomment to see coordinates
    # pygame.display.set_caption(str(enemy.rect) + str(player.rect))

    pygame.display.update()
    scr.update()
    # get events and move player
    EventList = pygame.event.get() 
    for e in EventList:
        if (e.type == KEYDOWN):
            k = pygame.key.get_pressed()
            # send keypresses to player
            tiled_map.player.read_keys(k)
            if (k[K_ESCAPE]):
                # menu
                print("menu called")
                M = Menu(scr)
                menureturn = M.menuloop()
                if (menureturn == 0):
                   running = False
                   pygame.quit() 
                   break
                if (menureturn == 2):
                    # next level
                    scr = Screen(800, 600)
                    screen = screen
                    tiled_map = level.next(tiled_map.player.get_pos())
                    tiled_map.render_map(scr.bg)
                    pygame.display.flip()
                    scr.top_msg.set_message("Level " + str(level.index))
        if (e.type == KEYUP):
            # send keyups too
            k = pygame.key.get_pressed()
            tiled_map.player.read_keys(k)
    # update level and if level is complete, load next one
    if (tiled_map.update_level()):
            # next level
            xy = tiled_map.player.get_pos()
            scr = Screen(800, 600)
            screen = screen
            tiled_map = level.next(xy)
            tiled_map.render_map(scr.bg)
            pygame.display.flip()
            scr.top_msg.set_message("Level " + str(level.index))
    clk.tick(fps)
