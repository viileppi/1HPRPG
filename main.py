#!/usr/bin/env python3
from os import path
import time
import pygame
from pygame.locals import *
import levelmanager
from vision import Screen
from menu import Menu
from menu import KeySetup
import userevents
import xml.etree.ElementTree as ET
import copy

# read settings
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

# init stuff
running = True
score = 0
## these settings are for 8bitdo sfc30
has_joystick = False
pygame.joystick.init()
if (pygame.joystick.get_count() > 0):
    joypad = pygame.joystick.Joystick(0)
    joypad.init()
    has_joystick = True
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

# level inits
level = levelmanager.LevelManager(scr)
maze = level.current_level

# map is rendered on background image
maze.render_map(scr.bg)

# set some variables
pygame.init()
lives_left = 3
start_again = False

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

def nextLevel():
    #scr = Screen(resolutionx, resolutiony)
    #screen = screen
    maze = level.next(score)
    maze.render_map(scr.bg)
    pygame.display.flip()
    scr.top_msg.set_message("Level " + str(level.xy) + " Lifes: " + str(lives_left) + " Score: " + str(score))

def menuCall():
    # menu
    M = Menu(scr)
    menureturn = M.menuloop()
    if (menureturn == 1):
       running = False
       pygame.quit() 

bars()

while running:
    # uncomment to see coordinates
    # pygame.display.set_caption(str(enemy.rect) + str(player.rect))
    start = 0
    if (start_again):
        start_again = False
        maze = level.next(score)
        maze.render_map(scr.bg)
        pygame.display.flip()
        scr.top_msg.set_message("Level " + str(level.xy) + " Lifes: " + str(lives_left) + " Score: " + str(score))

    if (maze.update_level()):
        # next level
        maze = level.next(score)
        maze.render_map(scr.bg)
        pygame.display.flip()
        scr.top_msg.set_message("Level " + str(level.xy) + " Lifes: " + str(lives_left) + " Score: " + str(score))

    if (lives_left < 0):
        pygame.time.wait(500)
        M = Menu(screen)
        M.menuitems = {"try again?": 0,
                        "quit": 1
                        }
        mr = M.menuloop()
        if (mr == 0):
            lives_left = 3
            score = 0
            level.difficulty = 1
            start_again = True
        if (mr == 1):
            pygame.quit()
            pygame.display.quit()
            running = False
            break

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
        if (e.type == QUIT):
            running = False
            pygame.quit()
            pygame.display.quit()
            break
        if (e.type == JOYBUTTONDOWN) or (e.type == JOYAXISMOTION):
            start = joypad.get_button(11)
            select = joypad.get_button(10)
            x_button = joypad.get_button(3)
            y_button = joypad.get_button(4)
            a_button = joypad.get_button(0)
            b_button = joypad.get_button(1)
            if (start * select == 1):
                running = False
                pygame.display.quit()
                pygame.quit()
                break
            if (start):
                menuCall()
            else:
                jp = {0: a_button, 1: b_button, 3: x_button, 4: y_button}
                x_axis = joypad.get_axis(0)
                y_axis = joypad.get_axis(1)
                maze.player.read_keys(None, (x_axis, y_axis), jp)
        if (e.type == KEYDOWN):
            k = pygame.key.get_pressed()
            # send keypresses to player
            maze.player.read_keys(k, None, None)
            if (k[K_BACKSPACE]):
                running = False
                pygame.display.quit()
                pygame.quit()
                break
            if (k[K_ESCAPE]):
                menuCall()
        if (e.type == KEYUP):
            # send keyups too
            k = pygame.key.get_pressed()
            maze.player.read_keys(k, None, None)
        if (e.type == player_died):
            # player dead
            bars()
            lives_left -= 1
            start_again = True
            scr.top_msg.set_message("Level " + str(level.xy) + " Lifes: " + str(lives_left) + " Score: " + str(score))

    if (running):
        pygame.display.update()
        scr.update()
        clk.tick(fps)

print("game over")
time.sleep(1)
