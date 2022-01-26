import pygame

PAD = 10                                # 間隔
SIZE = 30                               # ブロックの一辺

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, status):
        super().__init__()
        self.x = x
        self.y = y
        self.status = status
        self.is_flag = False
        self.is_open = False
        if not self.is_open:            # 開けていない時
            self.image = pygame.image.load("./images/block.png")
        self.rect = pygame.Rect(self.x * SIZE + PAD, self.y * SIZE + PAD + SIZE, self.image.get_width(), self.image.get_height())

    def open(self, user_map):
        #global user_map
        user_map[self.y][self.x] = 1
        self.is_open = True
        if self.is_open:
            self.image = pygame.image.load(f"./images/{self.status}.png")
        return user_map
    
    def flag(self, user_map):
        #global collect_flag_count
        user_map[self.y][self.x] = -1
        self.is_flag = True
        if self.is_flag:
            self.image = pygame.image.load("./images/flag.png")
        return user_map

    def unflag(self, user_map):
        user_map[self.y][self.x] = 0
        self.is_flag = False
        if not self.is_flag:
            self.image = pygame.image.load("./images/block.png")
        return user_map