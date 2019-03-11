import pygame
from pygame.locals import *
from objects import Object
import pytmx
from pytmx.util_pygame import load_pygame
import maptest
# from sprite_strip_anim import SpriteStripAnim

def init_screen(width, height):
    pygame.init()
    """ Set the screen mode
    This function is used to handle window resize events
    """
    return pygame.display.set_mode((width, height), pygame.RESIZABLE)

screen = init_screen(800, 640)
screen.set_colorkey(SRCALPHA)
tiled_map = maptest.TiledRenderer("testmap.tmx")
# player = Animator(screen, "juoksu2.png", 2)
bg = pygame.image.load("alpha_fill.png").convert_alpha()
mygroup = pygame.sprite.Group()
player = Object(screen, "juoksu3.png", (120,120), mygroup)
enemy = Object(screen, "juoksu3.png", (10,10), mygroup)
fill_a = Color(0,0,0,2)
running = True
pygame.init()
where_to = (0,0)
clk = pygame.time.Clock()
fps = 60
enemy.move((1,0))
player.move((0,0))
pygame.display.update()
tiled_map.render_map(bg)
while running:
    # cropped.blit(image, image_pos)
    # screen.fill(fill_a)
    screen.blit(bg, (0,0))
    enemy.patrol()
    player.move(where_to)
    # screen.blit(image, image_pos, image_crop)
    pygame.display.update()
    EventList = pygame.event.get() 
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
    clk.tick(fps)
