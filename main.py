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
from hud import HUD
import levelmanager
# from sprite_strip_anim import SpriteStripAnim

def init_screen(width, height):
    pygame.init()
    """ Set the screen mode
    This function is used to handle window resize events
    """
    return pygame.display.set_mode((width, height), pygame.RESIZABLE)

top_msg = HUD((8,0), 48, Color("yellow"), "Level 0")
screen = init_screen(800, 640)
screen.set_colorkey(SRCALPHA)
level = levelmanager.LevelManager(screen)
tiled_map = level.current_level
## using semi-transparent image for clearing the screen and smoothing out animation
bg = pygame.image.load(path.join("images", "alpha_fill.png")).convert_alpha()
# map is rendered on background image
tiled_map.render_map(bg)
ammogroup = pygame.sprite.Group()
finish = tiled_map.finish
running = True
pygame.init()
where_to = (0,0)
old_where = (0,0)
clk = pygame.time.Clock()
fps = 60
tiled_map.player.move((0,0))
cooldown = 200
shot = 0
pygame.key.set_repeat(50,50)
pygame.display.update()
# fills to show rects
#player.image.fill(Color("blue"))
#enemy.image.fill(Color("blue"))

def shoot(where):
    s = shot
    if (pygame.time.get_ticks() > s + cooldown):
        pew = Ammo(screen, path.join("images", "ammo.png"), (tiled_map.player.rect[0], tiled_map.player.rect[1]), where)
        ammogroup.add(pew)
        s = pygame.time.get_ticks()
    return s
while running:
    # uncomment to see coordinates
    # pygame.display.set_caption(str(enemy.rect) + str(player.rect))
    pygame.display.update()
    screen.blit(bg, (0,32))
    screen.blit(top_msg.image, (0,0))
    EventList = pygame.event.get() 
    # get events and move player
    for e in EventList:
        # if (e.type == KEYUP):
        #     if (where_to != (0,0)):
        #         old_where = where_to
        #     where_to = (0,0)
        if (e.type == KEYDOWN):
            k = pygame.key.get_pressed()
            if (k[K_ESCAPE] or k[K_q]):
                running = False
                pygame.quit()
                break
            if (k[K_p] and fps != 0):
                print("pause")
                old_fps = fps
                fps = 0
            elif (k[K_p] and fps == 0):
                print("continue")
                fps = old_fps
            if (k[K_z] and where_to != (0,0)):
                shot = shoot(where_to)
            elif (k[K_z] and where_to == (0,0)):
                shot = shoot(old_where)
            if (k[K_RIGHT]):
                where_to = (1,where_to[1])
            if (k[K_LEFT]):
                where_to = (-1,where_to[1])
            if (k[K_UP]):
                where_to = (where_to[0],-1)
            if (k[K_DOWN]):
                where_to = (where_to[0],1)
            if (where_to != (0,0)):
                old_where = where_to
        if (e.type == KEYUP):
            if (where_to != (0,0)):
                old_where = where_to
            if (k[K_RIGHT]):
                where_to = (0,where_to[1])
            if (k[K_LEFT]):
                where_to = (0,where_to[1])
            if (k[K_UP]):
                where_to = (where_to[0],0)
            if (k[K_DOWN]):
                where_to = (where_to[0],0)
    tiled_map.move_player(where_to)

    tiled_map.enemygroup.update()
    tiled_map.spritelist.update()
    tiled_map.spritelist.draw(screen)
    tiled_map.mygroup.update()
    ammogroup.update()
    ammogroup.draw(screen)
    chr_coll = pygame.sprite.groupcollide(tiled_map.mygroup, tiled_map.enemygroup, True, True, colli_kill_both)
    amm_coll = pygame.sprite.groupcollide(tiled_map.enemygroup, ammogroup, False, False, colli_kill_l)
    amm_wall = pygame.sprite.groupcollide(ammogroup, tiled_map.spritelist, False, False, colli_kill_l)
    enm_wall = pygame.sprite.groupcollide(tiled_map.enemygroup, tiled_map.spritelist, False, False, colli_bounce)
    pla_fin = pygame.sprite.groupcollide(tiled_map.mygroup, tiled_map.waypoints, False, False, colli)
    pla_wall = pygame.sprite.groupcollide(tiled_map.mygroup, tiled_map.spritelist, False, False, colli_bounce)
    for c in chr_coll:
        c.destroy()
        del c
        level.index = 0
        tiled_map = level.next()
        tiled_map.render_map(bg)
        pygame.display.flip()
    for u in pla_fin:
        # next level
        tiled_map = level.next()
        tiled_map.render_map(bg)
        pygame.display.flip()
        top_msg.set_message("Level " + str(level.index))
    clk.tick(fps)
