from ammo import deltaAmmo
from ammo import Blast
from pygame.locals import *

speed = 2

aimx = lambda x : x * speed
aimy = lambda y : y * speed

keymaps = {
        0: {
    "keyh" : {
           K_RIGHT: aimx(1),
           K_LEFT: aimx(-1)
           },
    "keyv" : {
           K_UP: aimy(-1),
           K_DOWN: aimy(1)
           },
    "keya" : {
           K_LALT: deltaAmmo,
           K_SPACE: Blast
           }
    },
        1: {
    "keyh" : {
           K_d: aimx(1),
           K_a: aimx(-1)
           },
    "keyv" : {
           K_w: aimy(-1),
           K_s: aimy(1)
           },
    "keya" : {
           K_j: deltaAmmo, 
           K_k: Blast
           }
    }
    }
