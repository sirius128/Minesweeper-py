import pygame
import random
import numpy as np

from block import Block
from mouseclick import mouseClick

FPS = 40
SIZE = 30
PAD = 10
FONT_SIZE = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 状態遷移
STAGE_START = 1     # ゲーム開始前の状態
STAGE_GAME = 2      # ゲーム本体が開始した状態
STAGE_OVER = 3      # ゲームオーバーの状態
STAGE_CLEAR = 4     # ゲームをクリアした状態
STAGE_QUIT = 9      # ゲームを終了する状態

class Board():
    def __init__(self, NUM_WIDTH, NUM_HEIGHT, NUM_MINES):
        pygame.init()
        self.screen = pygame.display.set_mode((NUM_WIDTH * SIZE + PAD * 2, NUM_HEIGHT * SIZE + PAD + SIZE * 2))
        
        pygame.display.set_caption("Minesweeper Game")      # ウィンドウタイトルの設定
        
        self.clock = pygame.time.Clock()
        self.NUM_WIDTH = NUM_WIDTH
        self.NUM_HEIGHT = NUM_HEIGHT
        self.NUM_MINES = NUM_MINES
        self.font = pygame.font.SysFont(None, FONT_SIZE)    # フォントの設定
        self.X_CENTER = (NUM_WIDTH * SIZE + PAD * 2) / 2
        self.Y_CENTER = (NUM_HEIGHT * SIZE + PAD + SIZE * 2) / 2

        self.is_manual_open = False                         # 再起的に自動で開く場合と手動で開く場合を区別

        self.click = None                                   # クリックをNoneを初期化
    
    def create_stage(self):                                 # ステージ作成に係る処理をまとめた関数
        def configure_mines(self, map):                     # 地雷を配置
            x = random.randint(0, self.NUM_WIDTH-1)         # 乱数生成
            y = random.randint(0, self.NUM_HEIGHT-1)        
            map[y][x] = -1                                  # 乱数で生成した座標に地雷を配置
            if np.count_nonzero(map<0) < self.NUM_MINES:    # 地雷の数が指定数に満たしていなければ
                return configure_mines(self, map)           # 再起処理を行う
            else:                                           # 要件を満たしたら
                print(map)
                return map                                  # 作成した地図の配列を返す

        def count_mines(self, x, y):                        # 指定された座標の周囲に地雷が何個あるか数える
            num_around_mine = 0                             # カウント用変数を初期化
            for j in range(-1, 2):                          # y
                for i in range(-1, 2):                      # x
                    if not (i == 0 and j == 0):             # 中心以外の場所をカウントする
                        if i+x >= 0 and j+y >= 0 and i+x < self.NUM_WIDTH and j+y < self.NUM_HEIGHT:  # 参照先が範囲外でないことを確認する
                            if self.stage_map[j+y][i+x] == -1:   # 地雷だったら
                                num_around_mine += 1        # カウントを増やす
            return num_around_mine                          # 数を返す
        
        self.stage_map = np.zeros((self.NUM_HEIGHT, self.NUM_WIDTH), np.int)    # ステージの地図配列を指定された大きさで0で初期化
        self.stage_map = configure_mines(self, self.stage_map)                  # 地雷を配置
        self.user_map = np.zeros_like(self.stage_map, np.int)                   # ユーザが操作したものを管理する地図配列を0で、stage_mapと同じ大きさで初期化

        for y, line in enumerate(self.stage_map):           # y。stage_mapの1つずつに処理
            for x, elem in enumerate(line):                 # x
                if elem != -1:                              # 地雷でなければ
                    self.stage_map[y][x] = count_mines(self, x, y)       # 周囲の地雷の数を数える
        
        self.blocks = pygame.sprite.Group()                 # ブロック格納用グループの作成
        for y, line in enumerate(self.stage_map):           # y。stage_mapの1つずつに処理
            for x, elem in enumerate(line):                 # x
                self.blocks.add(Block(x, y, elem))          # ブロック管理用Spriteを追加する
    
    def open_next(self, x, y, is_manual_open = False):      # ブロックをを開く関数。隣が空白なら連続して開ける
        if not self.user_map[y][x] or is_manual_open:       # まだ空いていなかったら継続。手動で開けた時は開ける
            if not self.stage_map[y][x] == -1 or is_manual_open:   # 爆弾じゃなかったら継続。手動で開けた時も開ける
                if x >= 0 and y >= 0 and x < self.NUM_WIDTH and y < self.NUM_HEIGHT:  # 参照先が範囲内なのを確認
                    for sprite in self.blocks.sprites():
                        if sprite.x == x and sprite.y == y:
                            self.user_map = sprite.unflag(self.user_map)
                            self.user_map = sprite.open(self.user_map)
                            if sprite.is_flag:              # 自動で開けた時に、flagが立てられていた時の処理
                                sprite.is_flag = False      # フラグを取る
                                self.flag_count -= 1        # フラグの数を1減らす
                            break
                    if self.stage_map[y][x] == 0:
                        for j in range(-1, 2):          # y
                            for i in range(-1, 2):      # x
                                if not (i == 0 and j == 0):   # 中心以外の場所
                                    if x+i >= 0 and y+j >= 0 and x+i < self.NUM_WIDTH and y+j < self.NUM_HEIGHT:  # 参照先が範囲内
                                        # print("call open_next()", x+i, y+j)
                                        self.open_next(x+i, y+j)    # 指定した座標を開ける
            else:
                return
        else:
            return
    
    def setup(self):                                        # ゲーム開始時の処理をまとめた関数
        self.flag_count = 0                                 # 立てたフラグを数える
        self.is_first_open = True                           # 初期開始時のみの処理を行うためのフラグ
        self.game_status = STAGE_START                      # ゲームの状態を指定
        self.create_stage()                                 # マップを生成する
        # print(self.stage_map)
        self.screen.fill(WHITE)                             # 画面を白で埋める
    
    def show_text(self, message, y):                        # テキスト表示処理をまとめた関数
        text = self.font.render(message, True, BLACK, WHITE)
        position = text.get_rect()                          # 位置を取得
        position.center = (self.X_CENTER, y)                # 位置を中央, 指定した座標に指定
        self.screen.blit(text, position)                    # 文字を転送する
    
    def show_timer(self):                                   # タイマー表示に係る処理
        timer = (pygame.time.get_ticks() - self.start_time) // 1000     # 基準時刻からの経過tickをミリ秒から秒にする
        text = self.font.render(f"{timer // 60:02}:{timer % 60:02} ", True, BLACK, WHITE)   # 何分何秒の表示にする
        self.screen.blit(text, (5, 5))                      # 文字を転送する。位置は左上
    
    def show_flag_count(self):                              # フラグのカウント表示に係る処理
        text = self.font.render(f" Flag: {self.flag_count:02}/{self.NUM_MINES:02}", True, BLACK, WHITE)     # 何分の何という表示をする
        position = text.get_rect()                          # 位置を取得
        position.y = 5                                      # 位置を設定
        position.right = (self.NUM_WIDTH * SIZE + PAD * 2) - 5  # 位置を右寄せにする
        self.screen.blit(text, position)                    # 文字を転送する
        
    def start(self):                                        # ゲームの開始前の実行に係る処理
        while self.game_status == STAGE_START:              # ゲームの状態がゲーム実行時なら。以下ループ
            for event in pygame.event.get():                # イベント取得
                if event.type == pygame.QUIT:               # 閉じるが押されたら
                    self.game_status = STAGE_QUIT           # ゲームの状態を終了状態にする
                elif event.type == pygame.KEYDOWN:          # キーが押されたら
                    if event.key == pygame.K_SPACE:         # キーがSpaceだったら
                        self.game_status = STAGE_GAME       # ゲームの状態を開始状態にする
                elif event.type == pygame.MOUSEBUTTONDOWN:  # マウスが押されたら
                    if event.button == 1:                   # 左クリックだったら
                        self.game_status = STAGE_GAME       # ゲームの状態を開始状態にする
            
            self.clock.tick(FPS)
            self.show_text("Press \"Space\" or Click to Start", self.Y_CENTER)  # 開始時の案内を表示する
            pygame.display.flip()
            self.screen.fill(WHITE)                         # 白で背景を埋める
        # self.game_status = STAGE_GAME

    def game(self):                                         # ゲーム本編に係る処理
        self.start_time = pygame.time.get_ticks()           # ゲーム開始時の基準時刻を取得
        while self.game_status == STAGE_GAME:               # ゲームの状態がゲーム開始なら。以下ループ
            for event in pygame.event.get():                # イベント取得
                if event.type == pygame.QUIT:               # 閉じるが押されたら
                    self.game_status = STAGE_QUIT           # ゲームの状態を終了状態にする
                elif event.type == pygame.MOUSEBUTTONDOWN:  # マウスが押されたら
                    # print("clicked", event.pos)
                    if event.button == 1:                   # 左クリックだったら
                        x, y = event.pos                    # 座標取得
                        self.click = mouseClick(x, y, 1)    # clickに座標とボタンの情報を格納したSpriteを格納
                    elif event.button == 3:                 # 右クリックだったら
                        x, y = event.pos                    # 座標取得
                        self.click = mouseClick(x, y, 3)    # clickに座標とボタンの情報を格納したSpriteを格納

            self.clock.tick(FPS)
            
            try:                                                            # clickが存在する時のみ
                collided = pygame.sprite.spritecollide(self.click, self.blocks, False)  # clickとブロックの衝突判定
                if collided:                                                # もし衝突（クリック）していたら
                    if self.click.status == 1:                              # 左クリックの時
                        for i in collided:                                  # 衝突していたSpriteを特定
                            if not i.is_flag:                               # フラグが立っていないことを確認
                                if self.is_first_open:                      # 最初に開ける時のみ。空白を開けるようにする
                                    while self.stage_map[i.y][i.x] != 0:    # 指定した座標が0（空白）になるまで
                                        print("create_stage")
                                        self.create_stage()                 # マップの再生成を行う
                                    self.is_first_open = False              # 初回ではなくなるので、フラグを変更する
                                    
                                self.open_next(i.x, i.y, True)              # 指定した座標を、手動で開けたとして関数を呼ぶ
                                if self.stage_map[i.y][i.x] == -1:          # 爆弾を開けた時
                                    self.game_status = STAGE_OVER           # ゲームの状態をゲームオーバーにする
                    elif self.click.status == 3:                            # 右クリックの時
                        for i in collided:                                  # 衝突していたSpriteを特定
                            if not i.is_open:                               # 空いていないことを確認
                                if i.is_flag:                               # フラグが立っていれば
                                    self.flag_count -= 1                    # フラグの数を1減らす
                                    self.user_map = i.unflag(self.user_map) # フラグを外す。地図の情報を書き換えるため、引数で渡して受け取る
                                else:                                       # フラグが立っていなければ
                                    if self.flag_count < self.NUM_MINES:    # フラグの数が上限に達していなければ
                                        self.flag_count += 1                # フラグの数を1増やす
                                        self.user_map = i.flag(self.user_map)   # フラグをつける。地図の情報を書き換えるため、引数で渡して受け取る
            except:
                pass

            self.blocks.draw(self.screen)                                   # blocksを描画する
            self.show_timer()                                               # timerを描画する
            self.show_flag_count()                                          # flag countを描画する
            
            # クリア判定処理
            if ((self.user_map > 0) == (self.stage_map > -1)).all():        # 爆弾以外のマスが全て開いているか
                if ((self.user_map < 0) == (self.stage_map < 0)).all():     # 爆弾のマスにフラグが立っているか
                    self.game_status = STAGE_CLEAR                          # ゲームの状態をクリアにする
            
            pygame.display.flip()
            # self.screen.fill(WHITE)

            self.click = None                                               # クリックを最後に初期化する
    
    def over(self):                                             # ゲームオーバー後に係る処理
        while self.game_status == STAGE_OVER:                   # ゲームの状態がゲームオーバーなら。以下ループ
            for event in pygame.event.get():                    # イベント取得
                if event.type == pygame.QUIT:                   # 閉じるが押されたら
                    self.game_status = STAGE_QUIT               # ゲームの状態を終了状態にする
                elif event.type == pygame.KEYDOWN:              # キーが押されたら
                    if event.key == pygame.K_SPACE:             # キーがSpaceだったら
                        self.game_status = STAGE_GAME           # ゲームの状態を開始状態にする
                        self.setup()                            # ゲーム開始処理を呼ぶ
                elif event.type == pygame.MOUSEBUTTONDOWN:      # マウスが押されたら
                    if event.button == 1:                       # 左クリックだったら
                        self.game_status = STAGE_GAME           # ゲームの状態を開始状態にする
                        self.setup()                            # ゲームの開始処理を呼ぶ
            
            self.clock.tick(FPS)
            #self.screen.fill(WHITE)
            self.show_text("Game Over.", self.Y_CENTER)         # 中央に表示
            self.show_text("Press \"Space\" or Click to Restart", self.Y_CENTER + FONT_SIZE)    #　中央+FONT_SIZE下に表示
            pygame.display.flip()
    
    def clear(self):                                            # ゲームクリア後に係る処理
        while self.game_status == STAGE_CLEAR:                  # ゲームの状態がクリアなら。以下ループ
            for event in pygame.event.get():                    # イベント取得
                if event.type == pygame.QUIT:                   # 閉じるが押されたら
                    self.game_status = STAGE_QUIT               # ゲームの状態を終了状態にする
                elif event.type == pygame.KEYDOWN:              # キーが押されたら
                    if event.key == pygame.K_SPACE:             # キーがSpaceだったら
                        self.game_status = STAGE_GAME           # ゲームの状態を開始状態にする
                        self.setup()                            # ゲーム開始処理を呼ぶ
                elif event.type == pygame.MOUSEBUTTONDOWN:      # マウスが押されたら
                    if event.button == 1:                       # 左クリックだったら
                        self.game_status = STAGE_GAME           # ゲームの状態を開始状態にする
                        self.setup()                            # ゲーム開始処理を呼ぶ
                
            self.clock.tick(FPS)
            #self.screen.fill(WHITE)
            self.show_text("Congraturations!!", self.Y_CENTER)  # 中央に表示する
            self.show_text("Press \"Space\" or Click to Restart", self.Y_CENTER + FONT_SIZE)    # 中央+FONT_SIZE下に表示
            pygame.display.flip()
    
    def run(self):
        while self.game_status != STAGE_QUIT:
            if self.game_status == STAGE_START:
                self.start()
            if self.game_status == STAGE_GAME:
                self.game()
            if self.game_status == STAGE_OVER:
                self.over()
            if self.game_status == STAGE_CLEAR:
                self.clear()