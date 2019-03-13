# -*- coding: UTF-8 -*-     
import objects

class Enemy(objects.Object):
    def __init__(self, screen, image, coords):
        """ image should be a spritesheet of square sprites """
        objects.Object.__init__(self, screen, image, coords)
        self.forward = True
        self.walked = 0
        self.walk_dist = 100
        self.where = (1,0)

    def patrol(self):
        coords = (0,0)
        if (self.forward):
            coords = (1, 0)
            self.walked += 1
        if (self.walked > self.walk_dist):
            self.forward = False
        if ((not self.forward)):
            coords = (-1, 0)
            self.walked -= 1
        if (self.walked < 0):
            self.forward = True
        self.move(coords)

    def seek(self):
        self.walked += 1
        if (self.walked > self.walk_dist):
            self.turnaround()
            self.walked = 0
        self.move(self.where)

    def turnaround(self):
        self.forward = not self.forward
        # self.walked = 1
        if (self.where == (1,0)):
            self.where = (0,1)
        elif (self.where == (0,1)):
            self.where = (-1,0)
        elif (self.where == (0,-1)):
            self.where = (1,0)
        elif (self.where == (-1,0)):
            self.where = (0,-1)
        elif (self.where == (0,0)):
            self.where = (1,0)
        self.move((self.where[0] * 4, self.where[1] * 4))




    def update(self):
        self.seek()

