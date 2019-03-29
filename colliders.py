# -*- coding: UTF-8 -*-     
from pygame import sprite
from pygame import math

def colli(l, r):
    # testfunction for collision callbacks
    if (sprite.collide_mask(l, r) != None):
        return True
    else:
        return False

def colli_basic(l, r):
    # testfunction for collision callbacks
    if (sprite.collide_rect(l, r)):
        return True
    else:
        return False

def colli_bounce(l, r):
    # testfunction for collision callbacks
    if (sprite.collide_rect(l, r)):
        l.turnaround(r)
        return True
    else:
        return False

def colli_kill_both(l, r):
    # testfunction for collision callbacks
    if (sprite.collide_mask(l, r) != None):
        l.destroy()
        r.destroy()
        return True
    else:
        return False

def colli_kill_l(l, r):
    # testfunction for collision callbacks
    if (sprite.collide_rect(l, r)):
        l.destroy()
        del l
        return True
    else:
        return False
def colli_los(l, r):
    # testfunction for collision callbacks
    if (sprite.collide_rect(l, r)):
        l.destroy()
        print("hit")
        return True
    else:
        return False

def colli_circle(l, r):
    if (sprite.collide_mask(l, r) != None):
        l.destroy()
        return True
    else:
        return False

