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
enemy_ch = pygame.mixer.Channel(0)
player_ch = pygame.mixer.Channel(1)
pew_sound = pygame.mixer.Sound("sounds/pew.wav")
player_pew = pygame.mixer.Sound("sounds/wep.wav")
blast = pygame.mixer.Sound("sounds/blast.wav")
death = pygame.mixer.Sound("sounds/death.wav")

# setup framerate and keyboard repeat rate
clk = pygame.time.Clock()
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
pygame.init()
lives_left = 3
start_again = False

fps = 60

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
                    scr.top_msg.set_message("Level " + str(level.xy) + " Lifes: " + str(lives_left))
        if (e.type == KEYUP):
            # send keyups too
            k = pygame.key.get_pressed()
            tiled_map.player.read_keys(k)
        if (e.type == USEREVENT+1):
            player_ch.play(player_pew)
        if (e.type == USEREVENT+2):
            player_ch.play(blast)
        if (e.type == USEREVENT+3):
            enemy_ch.play(death)
        if (e.type == USEREVENT+4):
            enemy_ch.play(pew_sound)
    if (not tiled_map.player.can_blast):
        scr.bottom_msg.setBusy(2)
    if (tiled_map.player.can_blast):
        scr.bottom_msg.setAvailable(2)
    if (len(tiled_map.mygroup.sprites()) < 1):
        # player dead
        lives_left -= 1
        start_again = True
        scr.top_msg.set_message("Level " + str(level.xy) + " Lifes: " + str(lives_left))
    # update level and if level is complete, load next one
    if (tiled_map.update_level() or start_again):
            # next level
            start_again = False
            pygame.time.wait(500)
            xy = tiled_map.player.get_pos()
            scr = Screen(resolutionx, resolutiony)
            screen = screen
            tiled_map = level.next(xy)
            tiled_map.render_map(scr.bg)
            pygame.display.flip()
            scr.top_msg.set_message("Level " + str(level.xy) + " Lifes: " + str(lives_left))
    if (lives_left < 0):
        M = Menu(screen, tiled_map.player)
        M.menuitems = {"try again?": 0,
                        "quit": 1
                        }
        mr = M.menuloop()
        if (mr == 0):
            start_again = True
            lives_left = 3
        if (mr == 1):
            pygame.quit()
clk.tick(fps)
