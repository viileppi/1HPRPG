#!/usr/bin/env python3
import pygame
from pygame.locals import *
from objects import Object
import pytmx
from pytmx.util_pygame import load_pygame
import maptest
from ammo import Ammo 
# from sprite_strip_anim import SpriteStripAnim

def init_screen(width, height):
    pygame.init()
    """ Set the screen mode
    This function is used to handle window resize events
    """
    return pygame.display.set_mode((width, height), pygame.RESIZABLE)

# set up basic level
screen = init_screen(800, 640)
screen.set_colorkey(SRCALPHA)
# using semi-transparent image for clearing the screen and smoothing out animation
bg = pygame.image.load("alpha_fill.png").convert_alpha()
tiled_map = maptest.TiledRenderer("testmap.tmx")
# map is rendered on background image
tiled_map.render_map(bg)
player = Object(screen, "juoksu3.png", (10,20))
enemygroup = pygame.sprite.Group()
for y in range(10, 600, 200):
    for x in range(0, 700, 350):
        enemy = Object(screen, "juoksu3.png", (x,y))
        enemygroup.add(enemy)
mygroup = pygame.sprite.Group(player)
ammogroup = pygame.sprite.Group()
player.move((100,100))
running = True
pygame.init()
where_to = (0,0)
clk = pygame.time.Clock()
fps = 60
enemy.move((1,0))
player.move((0,0))
cooldown = 200
shot = 0
pygame.display.update()
# fills to show rects
#player.image.fill(Color("blue"))
#enemy.image.fill(Color("blue"))

def colli(l, r):
    # testfunction for collision callbacks
    if (pygame.sprite.collide_rect(l, r)):
        print("colbollsuparoll " + str(pygame.time.get_ticks()))
        l.destroy()
        r.destroy()
        return True
    else:
        return False

def shoot(where):
    s = shot
    if (pygame.time.get_ticks() > s + cooldown):
        pew = Ammo(screen, "ammo.png", (player.rect[0], player.rect[1]), where_to)
        ammogroup.add(pew)
        s = pygame.time.get_ticks()
    return s

while running:
    # uncomment to see coordinates
    # pygame.display.set_caption(str(enemy.rect) + str(player.rect))
    pygame.display.update()
    screen.blit(bg, (0,0))
    EventList = pygame.event.get() 
    # get events and move player
    for e in EventList:
        if (e.type == KEYUP):
            where_to = (0,0)
        if (e.type == KEYDOWN):
            if (e.key == K_ESCAPE or e.key == K_q):
                running = False
                pygame.quit()
                break
            elif (e.key == K_RIGHT):
                where_to = (1,where_to[1])
            elif (e.key == K_LEFT):
                where_to = (-1,where_to[1])
            elif (e.key == K_UP):
                where_to = (where_to[0],-1)
            elif (e.key == K_DOWN):
                where_to = (where_to[0],1)
            mods = pygame.key.get_mods()
            if (mods & KMOD_LSHIFT):
                shot = shoot(where_to)
    # enemy.patrol()
    enemygroup.update()
    player.move(where_to)
    ammogroup.update()
    ammogroup.draw(screen)
    c = pygame.sprite.spritecollide(player, enemygroup, False, colli)
    if (c != []):
        for i in c:
            i.image.fill(Color("blue"), i.rect) 
            i.draw()
    for w in tiled_map.spritelist:
        if (player.rect.colliderect(w)):
            # take a step back
            player.move((where_to[0] * -3, where_to[1] * -3))
        for e in enemygroup:
            if (e.rect.colliderect(w)):
                e.turnaround()
        for f in ammogroup:
            if  (f.rect.colliderect(w)):
                f.destroy()
    d = pygame.sprite.groupcollide(ammogroup, enemygroup, True, True, colli)
    clk.tick(fps)
