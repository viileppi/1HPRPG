import pygame

class LOS(pygame.sprite.Sprite):
    def __init__(self, screen, enemy, player, walls):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.player = player
        self.walls = walls
        self.surf = self.screen.copy()
        self.rect = pygame.draw.line(self.surf, pygame.Color("black"), enemy, self.player.get_pos(), 1)

    def draw(self, enemy):
        self.rect = pygame.draw.line(self.surf, pygame.Color("black"), enemy, self.player.get_pos(), 1)
        c = pygame.sprite.spritecollideany(self, self.walls)
        if (c != None):
            return False
        else:
            return True


