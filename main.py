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
        if (e.type == KEYDOWN):
            k = pygame.key.get_pressed()
            if (k[K_ESCAPE] or k[K_q]):
                running = False
                pygame.quit()
                break
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
        tiled_map.render_map(bg)
        pygame.display.flip()
    for u in pla_fin:
        # next level
        screen = init_screen(800, 640)
        screen.set_colorkey(SRCALPHA)
        tiled_map = level.next()
        tiled_map.render_map(bg)
        pygame.display.flip()
        top_msg.set_message("Level " + str(level.index))
    clk.tick(fps)
