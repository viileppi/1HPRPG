#!/usr/bin/env python3
from os import listdir
from os import path
import pygame
from pygame.locals import *
import maptest
from ammo import Ammo 
from colliders import *
import levelmanager
from vision import Screen
from menu import Menu
from menu import KeySetup
import userevents
import xml.etree.ElementTree as ET
import copy

tree = ET.parse("settings.xml")
root = tree.getroot().find("main")
resolutionx = int(root.find("resolutionx").text)
resolutiony = int(root.find("resolutiony").text)
sounds = (root.find("sounds").text == "True")
mixer_rate = int(root.find("mixer_rate").text)
mixer_bitdepth = int(root.find("mixer_bitdepth").text)
mixer_channels = int(root.find("mixer_channels").text)
mixer_buffer = int(root.find("mixer_buffer").text)
fps = int(root.find("fps").text)
key_rate = int(root.find("key_rate").text)
lives_left = int(root.find("lives_left").text)
# override
# sounds = False
# init stuff
running = True
score = 0
#sounds = False
#resolutionx = 800
#resolutiony = 600
scr = Screen(resolutionx, resolutiony)
screen = scr.screen
if (sounds):
    pygame.mixer.init(mixer_rate, mixer_bitdepth, mixer_channels, mixer_buffer)
    enemy_ch = pygame.mixer.Channel(0)
    player_ch = pygame.mixer.Channel(1)
    pew_sound = pygame.mixer.Sound(path.join("sounds", "pew.wav"))
    player_pew = pygame.mixer.Sound(path.join("sounds", "wep.wav"))
    blast = pygame.mixer.Sound(path.join("sounds", "blast.wav"))
    obj_death = pygame.mixer.Sound(path.join("sounds", "death.wav"))


# setup framerate and keyboard repeat rate
clk = pygame.time.Clock()
pygame.key.set_repeat(key_rate,key_rate)
pygame.display.update()

# start menu
kmapi = 0


start_menuitems = {
        "New game": 0,
        "Quit": 1,
        "Sounds on": 2,
        "Sounds off": 3,
        "Choose keymap": 4
        }

startmenu = Menu(scr)
startmenu.menuitems = start_menuitems
item = startmenu.menuloop()
while (item>1):
    item = startmenu.menuloop()
    print(item)
    if (item==2):
        sounds = True
    if (item==3):
        sounds = False
    if (item==4):
        foo = KeySetup(scr)
        bar = foo.menuloop()
if (item==1):
    running=False
# level inits
level = levelmanager.LevelManager(scr)
maze = level.current_level
backup_maze = copy.copy(maze)

# map is rendered on background image
maze.render_map(scr.bg)

# set some variables
pygame.init()
lives_left = 3
start_again = False

#fps = 60

# userevents setup
player_shot = userevents.player_shot_event().type
player_blast = userevents.player_blast_event().type
death = userevents.death_event().type
enemy_shot = userevents.enemy_shot_event().type
player_died = userevents.player_died().type
player_ran = userevents.player_ran().type
player_blast = userevents.player_blast().type

def bars():
    while(scr.load_animation()):
        pygame.display.update()
        clk.tick(fps)

bars()

while running:
    # uncomment to see coordinates
    # pygame.display.set_caption(str(enemy.rect) + str(player.rect))
    if (maze.update_level() or start_again):
            # next level
            bars()
            start_again = False
            xy = maze.player.get_pos()
            scr = Screen(resolutionx, resolutiony)
            screen = screen
            maze = level.next(xy)
            backup_maze = copy.copy(maze)
            maze.render_map(scr.bg)
            pygame.display.flip()
            scr.top_msg.set_message("Level " + str(level.xy) + " Lifes: " + str(lives_left) + " Score: " + str(score))
    if (lives_left < 0):
        #pygame.time.wait(500)
        M = Menu(screen)
        M.menuitems = {"try again?": 0,
                        "quit": 1
                        }
        mr = M.menuloop()
        if (mr == 0):
            start_again = True
            lives_left = 3
        if (mr == 1):
            pygame.quit()

    # get events and move player
    EventList = pygame.event.get() 
    for e in EventList:
        if (sounds):
                if (e.type == player_shot):
                    player_ch.play(player_pew)
                if (e.type == player_blast):
                    player_ch.play(blast)
                if (e.type == death):
                    enemy_ch.play(obj_death)
                    # add score
                    score += 100
                    scr.top_msg.set_message("Level " + str(level.xy) + " Lifes: " + str(lives_left) + " Score: " + str(score))
                if (e.type == enemy_shot):
                    enemy_ch.play(pew_sound)
        if (e.type == KEYDOWN):
            k = pygame.key.get_pressed()
            # send keypresses to player
            maze.player.read_keys(k)
            if (k[K_BACKSPACE]):
                running = False
                pygame.quit()
                break
            if (k[K_ESCAPE]):
                # menu
                M = Menu(scr)
                menureturn = M.menuloop()
                if (menureturn == 1):
                   running = False
                   pygame.quit() 
                   break
                if (menureturn == 2):
                    # restart level
                    bars()
                    scr = Screen(resolutionx, resolutiony)
                    screen = screen
                    maze = backup_maze
                    backup_maze = copy.copy(maze)
                    maze.render_map(scr.bg)
                    pygame.display.flip()
                    scr.top_msg.set_message("Level " + str(level.xy) + " Lifes: " + str(lives_left) + " Score: " + str(score))
        if (e.type == KEYUP):
            # send keyups too
            k = pygame.key.get_pressed()
            maze.player.read_keys(k)
        if (e.type == player_died):
            # player dead
            bars()
            lives_left -= 1
            start_again = True
            scr.top_msg.set_message("Level " + str(level.xy) + " Lifes: " + str(lives_left) + " Score: " + str(score))
    if (not maze.player.can_blast):
        scr.bottom_msg.setBusy(1)
    if (not maze.player.can_run):
        scr.bottom_msg.setBusy(0)
    if (maze.player.can_blast):
        scr.bottom_msg.setAvailable(1)
    if (maze.player.can_run):
        scr.bottom_msg.setAvailable(0)
    #if (len(maze.mygroup.sprites()) < 1):
    # update level and if level is complete, load next one
    pygame.display.update()
    scr.update()
    clk.tick(fps)
