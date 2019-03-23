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

scr = Screen(800, 600)
screen = scr.screen
level = levelmanager.LevelManager(screen)
tiled_map = level.current_level
# map is rendered on background image
tiled_map.render_map(scr.bg)
finish = tiled_map.finish
running = True
pygame.init()
clk = pygame.time.Clock()
fps = 60
tiled_map.player.move((0,0))
pygame.key.set_repeat(50,50)
pygame.display.update()

while running:
    # uncomment to see coordinates
    # pygame.display.set_caption(str(enemy.rect) + str(player.rect))
    pygame.display.update()
    scr.update()
    EventList = pygame.event.get() 
    # get events and move player
    for e in EventList:
        if (e.type == KEYDOWN):
            k = pygame.key.get_pressed()
            if (k[K_q]):
                running = False
                pygame.quit()
                break
            if (k[K_ESCAPE]):
                print("menu called")
                M = Menu(scr)
                M.menuloop()
            else:
                tiled_map.player.read_keys(k)
        if (e.type == KEYUP):
            k = pygame.key.get_pressed()
            tiled_map.player.read_keys(k)

    tiled_map.enemygroup.update()
    tiled_map.spritelist.update()
    tiled_map.spritelist.draw(screen)
    tiled_map.mygroup.update()
    tiled_map.waypoints.draw(screen)
    tiled_map.player.ammogroup.update()
    tiled_map.player.ammogroup.draw(screen)
    chr_coll = pygame.sprite.groupcollide(tiled_map.mygroup, tiled_map.enemygroup, True, True, colli_kill_both)
    amm_coll = pygame.sprite.groupcollide(tiled_map.enemygroup, tiled_map.player.ammogroup, False, False, colli_kill_l)
    amm_wall = pygame.sprite.groupcollide(tiled_map.player.ammogroup, tiled_map.spritelist, False, False, colli_kill_l)
    enm_wall = pygame.sprite.groupcollide(tiled_map.enemygroup, tiled_map.spritelist, False, False, colli_bounce)
    enm_wal2 = pygame.sprite.groupcollide(tiled_map.enemygroup, tiled_map.waypoints, False, False, colli_bounce)
    pla_fin = pygame.sprite.groupcollide(tiled_map.mygroup, tiled_map.waypoints, False, False, colli_basic)
    pla_wall = pygame.sprite.groupcollide(tiled_map.mygroup, tiled_map.spritelist, False, False, colli_bounce)
    for c in chr_coll:
        c.destroy()
        del c
        level.index = 0
        tiled_map = level.next()
        tiled_map.render_map(scr.bg)
        pygame.display.flip()
    for u in pla_fin:
        # next level
        scr = Screen(800, 600)
        screen = scr.screen
        tiled_map = level.next()
        tiled_map.render_map(scr.bg)
        pygame.display.flip()
        scr.top_msg.set_message("Level " + str(level.index))
    clk.tick(fps)
