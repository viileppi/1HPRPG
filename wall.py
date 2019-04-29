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
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass

    def draw(self, screen):
        #pygame.draw.line(self.image, self.color, self.start, self.end, 16)
        r = self.screen.blit(
                self.image, 
                self.rect, 
                self.rect
                )

    def get_pos(self):
        return self.rect.center

    def too_close(self, to):
        v1 = pygame.math.Vector2(self.get_pos())
        v2 = pygame.math.Vector2(to.get_pos())
        v3 = v1.distance_to(v2)
        return v3 < 200


class Finish(Wall):
    def __init__(self, screen, start, end):
        Wall.__init__(self, screen, start, end)
        self.color = pygame.Color("green")
        self.rect = pygame.draw.line(self.screen, self.color, start, end, 16)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)


