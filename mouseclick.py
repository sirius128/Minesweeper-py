import pygame

class mouseClick(pygame.sprite.Sprite):                 # マウスクリックを管理するSprite Class
    def __init__(self, x, y, status):
        super().__init__()
        self.x = x
        self.y = y
        self.status = status                            # クリックされたボタンを保持
        self.image = pygame.Surface((1, 1))             # 1x1のサイズに設定
        #self.image.fill((0, 0, 0))                      
        #self.image.set_alpha(0)
        self.rect = pygame.Rect(self.x, self.y, 1, 1)   # 範囲を指定