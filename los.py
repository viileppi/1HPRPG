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


