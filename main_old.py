from gc import collect
import pygame
import time
import numpy as np
import random
FPS = 40
SIZE = 30

NUM_MINES = 25

NUM_WIDTH = 20
NUM_HEIGHT = 10

PAD = 10

collect_flag_count = 0

is_manual_open = None

is_first_open = True

game_status = 0

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, status):
        super().__init__()
        self.x = x
        self.y = y
        self.status = status
        self.is_flag = False
        self.is_open = False
        if not self.is_open:        # 開けていない時
            self.image = pygame.image.load("./images/block.png")
        elif not self.is_flag:
            self.image = pygame.image.load("./images/flag.png")
        else:
            self.image = pygame.image.load(f"./images/{self.status}.png")
        self.rect = pygame.Rect(self.x * SIZE + PAD, self.y * SIZE + PAD + SIZE, self.image.get_width(), self.image.get_height())

    def open(self, is_map_open):
        is_map_open[self.y][self.x] = 1
        self.is_open = True
        if self.is_open:
            self.image = pygame.image.load(f"./images/{self.status}.png")
        if self.status == -1:
            pass    # 爆弾クリック時の処理
        return is_map_open
    
    def flag(self, collect_flag_count):
        self.is_flag = True
        if self.is_flag:
            self.image = pygame.image.load("./images/flag.png")
        if self.status == -1:
            collect_flag_count += 1
        return collect_flag_count
    
    def unflag(self):
        self.is_flag = False
        if not self.is_flag:
            self.image = pygame.image.load("./images/block.png")


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

def create_stage():
    def configure_mines(map):
        x = random.randint(0, NUM_WIDTH-1)
        y = random.randint(0, NUM_HEIGHT-1)
        map[y][x] = -1
        if np.count_nonzero(map<0) < NUM_MINES:
            return configure_mines(map)
        else:
            print(map)
            return map

    def count_mines(x, y):
        num_around_mine = 0
        for j in range(-1, 2):          # y
            for i in range(-1, 2):      # x
                if not (i == 0 and j == 0):   # 中心以外の場所をカウントする
                    if i+x >= 0 and j+y >= 0 and i+x < NUM_WIDTH and j+y < NUM_HEIGHT:  # 参照先が範囲外でないことを確認する
                        if stage_map[j+y][i+x] == -1:   # 地雷だったら
                            num_around_mine += 1        # カウントを増やす
        return num_around_mine
    
    global stage_map, is_map_open, blocks
    stage_map = np.zeros((NUM_HEIGHT, NUM_WIDTH), np.int)
    stage_map = configure_mines(stage_map)
    is_map_open = np.zeros_like(stage_map, np.int)

    for y, line in enumerate(stage_map):         # y
        for x, elem in enumerate(line):      # x
            if elem != -1:
                stage_map[y][x] = count_mines(x, y)       # 周囲の地雷の数を数える
    
    blocks = pygame.sprite.Group()
    for y, line in enumerate(stage_map):
        for x, elem in enumerate(line):
            blocks.add(Block(x, y, elem))


create_stage()
print(stage_map)


screen = pygame.display.set_mode((NUM_WIDTH * SIZE + PAD * 2, NUM_HEIGHT * SIZE + PAD + SIZE * 2))
clock = pygame.time.Clock()

"""blocks = pygame.sprite.Group()
click = None
for y, line in enumerate(stage_map):
    for x, elem in enumerate(line):
        blocks.add(Block(x, y, elem))"""

click = None

"""def open_next(x, y):
    #print("called open_next")
    for sprite in blocks.sprites():
        if sprite.x == x and sprite.y == y:     # 該当のsprite
            if sprite.status == -1:
                print("return -1")
                return
            if not x >= 0 and y >= 0 and x < NUM_WIDTH and y < NUM_HEIGHT:  # 参照先が範囲外であったら
                print("return out of range", x, y)
                return
            if sprite.is_open:
                print("return opened", sprite.x, sprite.y)
                return

            sprite.open()
            print("opened", x, y)

            if stage_map[y][x] == 0:
                print("continue")
                for j in range(-1, 2):          # y
                    for i in range(-1, 2):      # x
                        if not (i == 0 and j == 0):   # 中心以外の場所
                            if x+i >= 0 and y+j >= 0 and x+i < NUM_WIDTH and y+j < NUM_HEIGHT:  # 参照先が範囲内
                                print("call open_next()", x+i, y+j)
                                open_next(x+i, y+j)"""

def open_next(x, y, is_manual_open = False):
    global is_map_open
    if not is_map_open[y][x] or is_manual_open:   # まだ空いていなかったら継続。手動で開けた時は開ける
        if not stage_map[y][x] == -1 or is_manual_open:   # 爆弾じゃなかったら継続。手動で開けた時も開ける
            if x >= 0 and y >= 0 and x < NUM_WIDTH and y < NUM_HEIGHT:  # 参照先が範囲内なのを確認
                for sprite in blocks.sprites():
                    if sprite.x == x and sprite.y == y:
                        is_map_open = sprite.open(is_map_open)
                        break
                if stage_map[y][x] == 0:
                    for j in range(-1, 2):          # y
                        for i in range(-1, 2):      # x
                            if not (i == 0 and j == 0):   # 中心以外の場所
                                if x+i >= 0 and y+j >= 0 and x+i < NUM_WIDTH and y+j < NUM_HEIGHT:  # 参照先が範囲内
                                    print("call open_next()", x+i, y+j)
                                    open_next(x+i, y+j) 
        else:
            return
    else:
        return

done = False
while True:
    for event in pygame.event.get():        # イベント処理
        if event.type == pygame.QUIT:
            done = True
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("clicked", event.pos)
            if event.button == 1:   # 左クリック
                x, y = event.pos
                click = mouseClick(x, y, 1)
            elif event.button == 3: # 右クリック
                x, y = event.pos
                click = mouseClick(x, y, 3)

    if done:
        break

    clock.tick(FPS)
    
    try:
        screen.blit(click.image, click.rect)
    except:
        pass
    
    try:
        collided = pygame.sprite.spritecollide(click, blocks, False)
        if collided:
            if click.status == 1:
                for i in collided:
                    if not i.is_flag:
                        #i.open()
                        if is_first_open:       # 最初に開ける時のみ、空白を開けるようにする
                            while stage_map[i.y][i.x] != 0:
                                print("create_stage")
                                create_stage()
                            is_first_open = False
                            
                        open_next(i.x, i.y, True)
            elif click.status == 3:
                for i in collided:
                    if not i.is_open:
                        if i.is_flag:
                            i.unflag()
                        else:
                            collect_flag_count = i.flag(collect_flag_count)
    except:
        pass
    

    blocks.draw(screen)

    # ゲーム進行管理
    if game_status == 0:
        # ゲーム開始前
        pass
        
    if collect_flag_count == NUM_MINES:
        print("congraturations")
        break

    pygame.display.flip()
    screen.fill((255, 255, 255))

    click = None







