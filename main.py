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
# from sprite_strip_anim import SpriteStripAnim

def init_screen(width, height):
    pygame.init()
    """ Set the screen mode
    This function is used to handle window resize events
    """
    return pygame.display.set_mode((width, height), pygame.RESIZABLE)

def load_levels():
    """ Load levels and return list of them """
    k = []
    l = listdir("levels")
    for t in l:
        if (t.split(".")[1] == "tmx"):
            k.append(path.join("levels", t))
    print(k)
    return k

levels = load_levels()
level_n = 0
screen = init_screen(800, 640)
screen.set_colorkey(SRCALPHA)

def next_level():
    tiled_map = maptest.TiledRenderer(screen, levels[level_n])
    n = (level_n + 1) % len(levels)
    return [tiled_map, n]
# set up basic level
foo = next_level()
tiled_map = foo[0]
level_n = foo[1]
## using semi-transparent image for clearing the screen and smoothing out animation
bg = pygame.image.load(path.join("images", "alpha_fill.png")).convert_alpha()
# map is rendered on background image
tiled_map.render_map(bg)
ammogroup = pygame.sprite.Group()
finish = tiled_map.waypoints["finish"]
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
            if (k[K_RIGHT]):
                where_to = (0,where_to[1])
            if (k[K_LEFT]):
                where_to = (0,where_to[1])
            if (k[K_UP]):
                where_to = (where_to[0],0)
            if (k[K_DOWN]):
                where_to = (where_to[0],0)
            if (where_to != (0,0)):
                old_where = where_to
        tiled_map.player.move(where_to)

    tiled_map.enemygroup.update()
    tiled_map.spritelist.update()
    tiled_map.spritelist.draw(screen)
    tiled_map.player.update()
    ammogroup.update()
    ammogroup.draw(screen)
    chr_coll = pygame.sprite.groupcollide(tiled_map.mygroup, tiled_map.enemygroup, True, True, colli_kill_both)
    amm_coll = pygame.sprite.groupcollide(tiled_map.enemygroup, ammogroup, False, False, colli_kill_l)
    amm_wall = pygame.sprite.groupcollide(ammogroup, tiled_map.spritelist, False, False, colli_kill_l)
    enm_wall = pygame.sprite.groupcollide(tiled_map.enemygroup, tiled_map.spritelist, False, False, colli_bounce)
    pla_wall = pygame.sprite.groupcollide(tiled_map.mygroup, tiled_map.spritelist, False, False, colli_bounce)
    # framerate
    clk.tick(fps)
