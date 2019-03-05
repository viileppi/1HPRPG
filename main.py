import pygame
from pygame.locals import *
from animator import Animator
# from sprite_strip_anim import SpriteStripAnim

def init_screen(width, height):
    pygame.init()
    """ Set the screen mode
    This function is used to handle window resize events
    """
    return pygame.display.set_mode((width, height), pygame.RESIZABLE)

screen = init_screen(800, 600)
pygame.font.init()
player = Animator(screen, "juoksu2.png", Rect(0,0,128,128),2)
running = True
pygame.init()
where_to = (0,0)
clk = pygame.time.Clock()
fps = 60

while running:
    # cropped.blit(image, image_pos)
    pygame.display.update()
    if ((where_to != (0,0)) and player.move_player(where_to)):
        player.move_steps = player.move_len
    # screen.blit(image, image_pos, image_crop)
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
