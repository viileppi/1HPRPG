import pygame

class LOS(pygame.sprite.Sprite):
    def __init__(self, screen, enemy, source, walls):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.source = source
        self.walls = walls
        self.surf = self.screen.copy()
        self.rect = pygame.draw.line(self.surf, pygame.Color("black"), enemy, self.source.get_pos(), 1)
        # uncomment to see line of sight
        self.debug = False

    def colli(self, l, r):
        return pygame.sprite.collide_mask(l, r)

    def draw(self, enemy):
        if (self.debug):
            self.rect = pygame.draw.line(self.screen, pygame.Color("red"), enemy, self.source.get_pos(), 1)
        else:
            self.rect = pygame.draw.line(self.surf, pygame.Color("black"), enemy, self.source.get_pos(), 1)
        c = pygame.sprite.spritecollideany(self, self.walls)#, self.colli)
        if (c != None):
            return False
        else:
            return True

class Cast(pygame.sprite.Sprite):
    def __init__(self, screen, walls, source):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.walls = walls
        self.source = source
        self.ray_shrink = self.source.ray_shrink
        self.surf = self.screen.copy()
        self.pos = self.source.get_pos()
        self.ray_size = int(self.source.speed/2)
        self.color = pygame.Color("red")
        #self.left = (self.pos[0] - self.ray_len, self.pos[1])
        #self.right = (self.pos[0] + self.ray_len, self.pos[1])
        #self.up = (self.pos[0], self.pos[1] - self.ray_len)
        #self.down = (self.pos[0], self.pos[1] + self.ray_len)

    def test(self, to):
        self.pos = self.source.get_pos()
        ray_rect = self.source.rect.inflate(self.ray_shrink[0], self.ray_shrink[1])
        # ray_w = self.ray_w + abs(int(self.ray_w * to[0]))
        # ray_w = (1+abs(to[0])) * self.ray_w
        # ray_len = (1+abs(to[1])) * self.ray_size
        #ray_len = self.ray_size * (1+abs(to[1])/2)
        #ray_rect = self.source.rect.inflate(-self.ray_size, 0)
        #ray_rect = self.source.rect #.inflate(-self.size[0], -self.size[1])
        #ray_rect = self.source.rect.inflate(-24,-8)
        #self.ray_rect.move_ip(to[0] * self.ray_size, to[1] * self.ray_size)
        ray_rect.move_ip(to[0] * self.ray_size, to[1] * self.ray_size)
        ray = pygame.draw.rect(self.screen, self.color, ray_rect)

        if (ray_rect.collidelist(self.walls) == -1):
            return (1,1)
        else:
            return (to[0] - to[0],to[1] - to[1])

