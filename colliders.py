# -*- coding: UTF-8 -*-     
from pygame import sprite

def colli(l, r):
    # testfunction for collision callbacks
    if (sprite.collide_mask(l, r) != None):
        return True
    else:
        return False

def colli_bounce(l, r):
    # testfunction for collision callbacks
    p = sprite.collide_mask(l, r)
    if (p != None):
        l.turnaround(p)
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
    if (sprite.collide_mask(l, r) != None):
        l.destroy()
        return True
    else:
        return False

