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
running = True
resolutionx = 800
resolutiony = 600
scr = Screen(resolutionx, resolutiony)
screen = scr.screen

# setup framerate and keyboard repeat rate
clk = pygame.time.Clock()
fps = 60
pygame.key.set_repeat(100,100)
pygame.display.update()

# start menu
kmapi = 0
kmap_menuitems = {
            "arrow-keys and z": 0,
            "W,A,S,D and space": 1
             }

start_menuitems = {
        "New game": 0,
        "Quit": 1,
        "Choose keymap": 2
        }

startmenu = Menu(scr, None)
startmenu.menuitems = start_menuitems
sml = startmenu.menuloop()
if (sml == 1):
    running = False
    pygame.quit() 
if (sml == 2):
    kmenu = Menu(scr, None)
    kmenu.menuitems = kmap_menuitems
    kmapi = kmenu.menuloop()

# level inits
level = levelmanager.LevelManager(scr, kmapi)
tiled_map = level.current_level

# map is rendered on background image
tiled_map.render_map(scr.bg)

# set some variables
finish = tiled_map.finish
pygame.init()

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
            if (k[K_BACKSPACE]):
                running = False
                pygame.quit()
                break
            if (k[K_ESCAPE]):
                # menu
                print("menu called")
                M = Menu(scr, tiled_map.player)
                menureturn = M.menuloop()
                if (menureturn == 0):
                   running = False
                   pygame.quit() 
                   break
                if (menureturn == 2):
                    # next level
                    scr = Screen(resolutionx, resolutiony)
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
            scr = Screen(resolutionx, resolutiony)
            screen = screen
            tiled_map = level.next(xy)
            tiled_map.render_map(scr.bg)
            pygame.display.flip()
            scr.top_msg.set_message("Level " + str(level.index))
    clk.tick(fps)
