import pygame
import colliders

class LOS(pygame.sprite.Sprite):
    def __init__(self, source):
        pygame.sprite.Sprite.__init__(self)
        self.source = source
        self.screen = self.source.screen
        #self.walls = walls
        self.wallgroup = self.source.wallgroup
        self.walls = []
        for w in self.source.wallgroup.sprites():
            self.walls.append(w.rect)
        self.surf = self.screen.copy()
        self.color = pygame.Color("red")
        self.rect = pygame.draw.line(self.surf, self.color, self.source.player.get_pos(), self.source.get_pos(), 1)
        self.image = pygame.Surface((self.rect.width, self.rect.height))

    def colli(self, l, r):
        return pygame.sprite.collide_mask(l, r) == None

    def draw(self):
        self.rect = pygame.draw.line(self.surf, self.color, self.source.get_pos(), self.source.player.get_pos(), 1)
        #self.image = pygame.Surface((self.rect.width, self.rect.height))
        #self.mask = pygame.mask.from_surface(self.surf)
        #self.image = pygame.Surface((self.rect.width, self.rect.height))
        #print(c)
        #return False
        c = pygame.sprite.spritecollideany(self, self.wallgroup)#, self.colli)
        if (c != None):
            return False
        else:
            return True

class Cast(pygame.sprite.Sprite):
    def __init__(self, source):
        pygame.sprite.Sprite.__init__(self)
        self.source = source
        self.walls = []
        for w in self.source.wallgroup.sprites():
            self.walls.append(w.rect)
        self.screen = source.screen
        self.ray_shrink = self.source.ray_shrink
        self.surf = self.screen.copy()
        self.pos = self.source.get_pos()
        #self.ray_size = int(self.source.speed/2)
        self.ray_size = 2
        self.color = pygame.Color("red")
        #self.left = (self.pos[0] - self.ray_len, self.pos[1])
        #self.right = (self.pos[0] + self.ray_len, self.pos[1])
        #self.up = (self.pos[0], self.pos[1] - self.ray_len)
        #self.down = (self.pos[0], self.pos[1] + self.ray_len)

    def colli(self, l, r):
        return pygame.sprite.collide_mask(l, r)

    def test(self, to):
        self.pos = self.source.rect
        ray_rect = self.source.rect.inflate(self.ray_shrink[0], self.ray_shrink[1])
        ray_rect.move_ip((to[0]*self.ray_size, to[1]*self.ray_size))
        #ray = pygame.draw.rect(self.screen, self.color, ray_rect)
        #if (pygame.sprite.spritecollideany(self.source, self.source.wallgroup, self.colli) == None):
        #c = pygame.sprite.spritecollideany(self.source, self.source.wallgroup, self.colli)
        #c = pygame.sprite.spritecollideany(self.source, self.walls)#, pygame.sprite.collide_mask)
        c = ray_rect.collidelist(self.walls)
        if (c == -1):
            self.source.rect = self.pos
            return (1,1)
        else:
            self.source.rect = self.pos
            return (to[0] - to[0],to[1] - to[1])

