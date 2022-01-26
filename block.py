import pygame

PAD = 10                                # 間隔
SIZE = 30                               # ブロックの一辺

class Block(pygame.sprite.Sprite):      # ブロックを管理するSprite Class
    def __init__(self, x, y, status):
        super().__init__()
        self.x = x
        self.y = y
        self.status = status
        self.is_flag = False            # フラグが立っているか
        self.is_open = False            # 開いているか
        if not self.is_open:            # 開けていない時
            self.image = pygame.image.load("./images/block.png")    # 画像を読み込む
        self.rect = pygame.Rect(self.x * SIZE + PAD, self.y * SIZE + PAD + SIZE, self.image.get_width(), self.image.get_height())   # 描画範囲を指定

    def open(self, user_map):           # 開くに係る処理
        user_map[self.y][self.x] = 1    # 引数で渡されたuser_mapに、開けたことを示す値を挿入
        self.is_open = True             # 開いたフラグを付与
        if self.is_open:                # 空いていたら
            self.image = pygame.image.load(f"./images/{self.status}.png")   # 画像を読み込む（変更する）
        return user_map                 # 引数で渡された配列を返す
    
    def flag(self, user_map):           # フラグを立てるに係る処理
        user_map[self.y][self.x] = -1   # 引数で渡されたuser_mapに、立てたことを示す値を挿入
        self.is_flag = True             # 立てたことを保持
        if self.is_flag:                # フラグが立っていれば
            self.image = pygame.image.load("./images/flag.png")             # 画像を読み込む（変更する）
        return user_map                 # 引数で渡された配列を返す

    def unflag(self, user_map):         # フラグを取るに係る処理
        user_map[self.y][self.x] = 0    # 引数で渡されたuser_mapに、取ったことを示す値を挿入
        self.is_flag = False            # 取ったことを保持
        if not self.is_flag:            # フラグが立っていなければ
            self.image = pygame.image.load("./images/block.png")            # 画像を読み込む（変更する）
        return user_map                 # 引数で渡された配列を返す