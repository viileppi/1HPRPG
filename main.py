#!/usr/bin/env python3
from os import path
import time
import pygame
from pygame.locals import *
import levelmanager
from vision import Screen
from menu import Menu
from menu import Tab
from menu import Choice
from menu import Adjust
from menu import Hiscore
import userevents
import xml.etree.ElementTree as ET
import copy
from info import Info
from readkeys import KeyReader

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
scr = Screen(resolutionx, resolutiony)
screen = scr.screenhas_joystick = False
pygame.joystick.init()
if (pygame.joystick.get_count() > 0):
    joypad = pygame.joystick.Joystick(0)
    joypad.init()
    has_joystick = True
myKeyReader = KeyReader()
keys = myKeyReader.readKeyDwn(pygame.key.get_pressed())

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

# setu up some functions to use with mainmenu
def restart():
    global lives_left
    lives_left = 3
    global score
    score = 0
    global start_again
    start_again = True
    global level
    level = levelmanager.LevelManager(scr)
    global maze
    maze = level.current_level

def Quit():
    global running
    running = False
    print("quit called from menu")
    pygame.event.post(pygame.event.Event(pygame.QUIT))

# setup mainmenu
M = Menu(scr.screen)
w = M.width
mainmenu = Tab(M.screen, "Main", 
[
    Choice(M.message, "Continue", w, lambda x : x),
Choice(M.message, "New game", w, restart),
Choice(M.message, "Quit", w, Quit),
Choice(M.message, "Difficulty: ", w, lambda x : x, ["casual, ", "medium, ", "hard"])
]
)
settings = Tab(M.screen, "Settings", 
[
    Choice(M.message, "Resolution: ", w, lambda x : x, ["320*240, ", "800*600"]), 
    Choice(M.message, "Audio: ", w, lambda x : x, ["on, ", "off"]), 
Adjust(M.message, "Volume: ", w, 0, 100, 70, 10)
]
)
info = Tab(M.screen, "Help", 
[
    Choice(M.message, "foobar", w, lambda x: x)
]
)
M.items = [mainmenu, settings, info]
M.menuloop()


def bars():
    while(scr.load_animation()):
        pygame.display.update()
        clk.tick(fps)
bars()

while running:
    # uncomment to see coordinates
    # pygame.display.set_caption(str(enemy.rect) + str(player.rect))
    start = 0
    if (start_again):
        start_again = False
        #maze = level.next(score)
        maze = level.again()
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
        mr = M.menuloop()
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
        if (e.type == JOYAXISMOTION) or (e.type == JOYBUTTONDOWN):
            keys = myKeyReader.readJoypad(joypad) 
            maze.player.read_keys(keys)
        if (e.type == KEYDOWN) or (e.type == KEYUP):
            keys = myKeyReader.readKeyDwn(pygame.key.get_pressed())
            maze.player.read_keys(keys)
        if (keys[1] == "menu"):
            mr = M.menuloop()
            mr()
        if (e.type == player_died):
            # player dead
            bars()
            lives_left -= 1
            start_again = True
            scr.top_msg.set_message("Level " + str(level.xy) + " Lifes: " + str(lives_left) + " Score: " + str(score))
        if (e.type == MOUSEBUTTONDOWN):
            mouse = myKeyReader.readMouse()
            maze.player.read_mouse(mouse)

    if (running):
        pygame.display.update()
        scr.update()
        clk.tick(fps)
h = Hiscore(scr.screen, None)
h.draw()


