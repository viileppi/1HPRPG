import pygame
from pygame.locals import *
from animator import Animator
from objects import Object
# from sprite_strip_anim import SpriteStripAnim

def init_screen(width, height):
    pygame.init()
    """ Set the screen mode
    This function is used to handle window resize events
    """
    return pygame.display.set_mode((width, height), pygame.RESIZABLE)

screen = init_screen(800, 600)
pygame.font.init()
# player = Animator(screen, "juoksu2.png", 2)
mygroup = pygame.sprite.Group()
enemygroup = pygame.sprite.Group()
player = Object(screen, "juoksu2.png", (30,30))
enemy = Object(screen, "juoksu2.png", (10,10))
player.move_animator.add2group(mygroup)
enemy.move_animator.add2group(enemygroup)
running = True
pygame.init()
where_to = (0,0)
clk = pygame.time.Clock()
fps = 60
enemy.move((0,0))
player.move((0,0))
pygame.display.update()
while running:
    # cropped.blit(image, image_pos)
    pygame.display.update()
    if ((where_to != (0,0)) and player.move(where_to)):
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
