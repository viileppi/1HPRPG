import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, screen, start, end):
        pygame.sprite.Sprite.__init__(self)
        self.start = start
        self.end = end
        self.screen = screen
        self.color = pygame.Color("blue")
        self.rect = pygame.draw.line(self.screen, self.color, start, end, 16)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)

    def update(self):
        r = self.screen.blit(
                self.image, 
                self.rect, 
                self.rect
                )

    def draw(self, screen):
        pygame.draw.line(self.image, self.color, self.start, self.end, 16)



