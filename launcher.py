import pygame
from mouseclick import mouseClick

FPS = 40
PAD = 50

SIZE = 100
FONT_SIZE = 30      

WIDTH = 500         
HEIGHT = 250

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GAME = [(10, 10, 8), (20, 12, 25), (22, 15, 50)]    # 項目ごとのゲームデータ。[(初級), (中級), (上級)]。(幅, 高さ, 爆弾)
                                                    # これをmain.pyに渡すことでゲームが開始される

def launcher():
    pygame.init()

    class Image(pygame.sprite.Sprite):      # 表示する画像を管理するImageクラスの定義
        def __init__(self, menu_num):
            super().__init__()
            self.image = pygame.image.load(f"./images/menu_{menu_num}.png")
            self.rect = pygame.Rect(PAD * menu_num + SIZE * (menu_num-1), PAD, self.image.get_width(), self.image.get_height())
            self.menu_num = menu_num

    screen = pygame.display.set_mode((WIDTH, HEIGHT))   # 画面の初期設定
    pygame.display.set_caption("Minesweeper Launcher")  # ウィンドウタイトルの設定
    clock = pygame.time.Clock()

    images = pygame.sprite.Group()          # 画像を一括管理するグループの作成
    for i in range(1, 4):
        images.add(Image(i))                # 1~3の画像を格納

    click = None                            # clickを管理する変数をNoneで初期化
    done = True                             # 無限ループ脱出用

    font = pygame.font.SysFont(None, FONT_SIZE) # 文字描画準備

    while done:
        for event in pygame.event.get():                # イベント取得
            if event.type == pygame.QUIT:               # 閉じるが押されたら
                done = False                            # 無限ループ脱出
            elif event.type == pygame.MOUSEBUTTONDOWN:  # マウスが押されたら
                if event.button == 1:                   # 左クリックだったら
                    x, y = event.pos                    # 座標取得
                    click = mouseClick(x, y, 1)         # clickにmouseClick Spriteを格納
            elif event.type == pygame.KEYDOWN:          # キーが押されたら
                if event.key == pygame.K_1:             # キーが1だったら
                    done = False
                    return GAME[0]                      # 初級のデータを返す
                elif event.key == pygame.K_2:           # キーが2だったら
                    done = False                        
                    return GAME[1]                      # 中級のデータを返す
                elif event.key == pygame.K_3:           # キーが3だったら
                    done = False
                    return GAME[2]                      # 上級のデータを返す
        
        try:                                            # clickが存在する時のみ
            collided = pygame.sprite.spritecollide(click, images, False)    # clickと画像の衝突判定
            if collided:                                # もし衝突（クリック）していたら
                for sprite in collided:                 # 衝突していたSpriteを特定
                    done = False
                    return GAME[sprite.menu_num - 1]    # クリックした難易度のデータを返す
        except:
            pass
        
        clock.tick(FPS)
        if pygame.time.get_ticks() % 1000 // 100 < 8:   # 1秒中0.8秒の間案内表示
            text = font.render("Type No. or Click to Start Minesweeper.", True, BLACK, WHITE)
            position = text.get_rect()
            position.center = (WIDTH /2, HEIGHT - FONT_SIZE)
            screen.blit(text, position)                 # text を screen に position の位置に転送する

        images.draw(screen)                             # images を描画する

        pygame.display.flip()
        screen.fill(WHITE)                              # 白で背景を埋める

if __name__ == "__main__":
    launcher()