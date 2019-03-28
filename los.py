import pygame

class LOS(pygame.sprite.Sprite):
    def __init__(self, screen, enemy, player, walls):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.player = player
        self.walls = walls
        self.surf = self.screen.copy()
        self.rect = pygame.draw.line(self.surf, pygame.Color("black"), enemy, self.player.get_pos(), 1)
        # uncomment to see line of sight
        self.debug = False

    def draw(self, enemy):
        if (self.debug):
            self.rect = pygame.draw.line(self.screen, pygame.Color("red"), enemy, self.player.get_pos(), 1)
        else:
            self.rect = pygame.draw.line(self.surf, pygame.Color("black"), enemy, self.player.get_pos(), 1)
        c = pygame.sprite.spritecollideany(self, self.walls)
        if (c != None):
            return False
        else:
            return True

class Cast(pygame.sprite.Sprite):
    def __init__(self, screen, walls, player):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.walls = walls
        self.player = player
        self.surf = self.screen.copy()
        self.pos = self.player.get_pos()
        self.ray_size = (16,32)
        self.ray_w = 32
        self.color = pygame.Color("red")
        #self.left = (self.pos[0] - self.ray_len, self.pos[1])
        #self.right = (self.pos[0] + self.ray_len, self.pos[1])
        #self.up = (self.pos[0], self.pos[1] - self.ray_len)
        #self.down = (self.pos[0], self.pos[1] + self.ray_len)

    def test(self, to):
        self.pos = self.player.get_pos()
        ray_w = self.ray_w + abs(int(self.ray_w * to[0]))
        self.ray = pygame.draw.line(self.surf, self.color, self.pos, (self.pos[0] + to[0] * self.ray_size[0], 
            self.pos[1] + to[1] * self.ray_size[1]), ray_w)

        if (self.ray.collidelist(self.walls) == -1):
            return (1,1)
        else:
            return (to[0] - to[0],to[1] - to[1])

