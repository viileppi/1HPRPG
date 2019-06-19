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
from menu import Text2Image
import userevents
import xml.etree.ElementTree as ET
import copy
from info import Info
from readkeys import KeyReader
from hiscore import Hiscore

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
p = Text2Image()
pressakey = p.make_image("press a key", 100)
# set some variables
pygame.init()
lives_left = 3
start_again = False


## these settings are for 8bitdo sfc30
reso = pygame.display.list_modes()
#scr = Screen(resolutionx, resolutiony)
scr = Screen(resolutionx, resolutiony)
#screen = scr.screenhas_joystick = False
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
    pygame.mixer.music.load(path.join("sounds", "song.xm"))


# setup framerate and keyboard repeat rate
clk = pygame.time.Clock()
pygame.key.set_repeat(key_rate,key_rate)
pygame.display.update()

# level inits
level = levelmanager.LevelManager(scr)
maze = level.current_level

# map is rendered on background image
maze.render_map(scr.bg)

# userevents setup
player_shot = userevents.player_shot_event().type
player_blast = userevents.player_blast_event().type
death = userevents.death_event().type
enemy_shot = userevents.enemy_shot_event().type
player_died = userevents.player_died().type
player_ran = userevents.player_ran().type
player_blast = userevents.player_blast().type
music_stop = userevents.music_stop().type
pygame.mixer.music.set_endevent(music_stop)


def start_music():
    pygame.mixer.music.load(path.join("sounds", "song.xm"))
    pygame.mixer.music.play()

def start_sung():
    pygame.mixer.music.load(path.join("sounds", "sing.xm"))
    pygame.mixer.music.play()

def bars():
    start_music()
    while(scr.load_animation()):
        pygame.display.update()
        clk.tick(30)

hs = Hiscore(scr.screen)
#r = scr.screen.blit(pressakey, (100,100))
def introduction():
    start_sung()
    stopped = True
    while stopped:
        pygame.time.wait(1500)
        hs.intro(800)
        pygame.display.update()
        EventList = pygame.event.get() 
        for e in EventList:
            if (e.type == music_stop):
                pygame.mixer.music.play()
            elif (e.type == KEYDOWN) or (e.type == JOYAXISMOTION):
                stopped = False
    bars()
introduction()
while running:
    # uncomment to see coordinates
    # pygame.display.set_caption(str(enemy.rect) + str(player.rect))
    start = 0
    if (start_again):
        start_again = False
        #maze = level.next(score)
        # tähän fps suoraan settings.xml:stä
        fps = int(root.find("fps").text)
        maze = level.again()
        maze.render_map(scr.bg)
        pygame.display.flip()
        scr.top_msg.set_message("Level " + str(level.xy) + " Lifes: " + str(lives_left) + " Score: " + str(score))

    if (maze.update_level()):
        # next level
        score += 247
        bars()
        fps = int(root.find("fps").text)
        fps += int(score/450)
        print(fps)
        maze = level.next(score)
        maze.render_map(scr.bg)
        pygame.display.flip()
        scr.top_msg.set_message("Level " + str(level.xy) + " Lifes: " + str(lives_left) + " Score: " + str(score))

    if (lives_left < 0):
        # init stuff
        pygame.event.clear()
        stopped = True
        scr = Screen(resolutionx, resolutiony)
        #hs.input(score)
        #hs.draw()
        pygame.display.update()
        running = True
        score = 0
        # set some variables
        lives_left = 3
        start_again = True
        maze = level.next(score)
        #name = hs.alphabet_input(score)
        #print(name)
        #hs.add(name[0],name[1])
        ### mr = M.menuloop()
    # get events and move player
    EventList = pygame.event.get() 
    for e in EventList:
        if (sounds):
            if (e.type == music_stop):
                #maze.generate_maze(maze.screen)
                # current level must be finished before song ends
                # player dead
                bars()
                pygame.display.update()
                lives_left -= 1
                start_again = True
                scr.top_msg.set_message("Level " + str(level.xy) + " Lifes: " + str(lives_left) + " Score: ")
                start_music()
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
            lives_left = lives_left = -1
            #pygame.quit()
            #pygame.display.quit()
            break
        if (e.type == JOYAXISMOTION) or (e.type == JOYBUTTONDOWN):
            keys = myKeyReader.readJoypad(joypad) 
            maze.player.read_keys(keys)
        if (e.type == KEYDOWN) or (e.type == KEYUP):
            keys = myKeyReader.readKeyDwn(pygame.key.get_pressed())
            maze.player.read_keys(keys)
        if (keys[1] == "menu"):
            pass
            ### mr = M.menuloop()
            ### mr()
        if (e.type == player_died):
            # player dead
            bars()
            pygame.display.update()
            lives_left -= 1
            start_again = True
            scr.top_msg.set_message("Level " + str(level.xy) + " Lifes: " + str(lives_left) + " Score: ")
        if (e.type == MOUSEBUTTONDOWN):
            mouse = myKeyReader.readMouse()
            maze.player.read_mouse(mouse)

    if (running):
        pygame.display.update()
        scr.update()
        clk.tick(fps)
        #fps = min(90, fps + (clk.tick(fps)/1667))
        #secs = int(pygame.time.get_ticks()/100)
        #if ((secs%10) == 0) and (fps<69):
        #    fps = min(70, fps + 1)
        #    #print("secs: " + str(secs) + "|fps: " + str(fps))

pygame.quit()
pygame.display.quit()
 
