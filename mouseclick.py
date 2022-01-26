import pygame

class mouseClick(pygame.sprite.Sprite):
    def __init__(self, x, y, status):
        super().__init__()
        self.x = x
        self.y = y
        self.status = status
        self.image = pygame.Surface((1, 1))
        self.image.fill((0, 0, 0))
        #self.image.set_alpha(0)
        self.rect = pygame.Rect(self.x, self.y, 1, 1)