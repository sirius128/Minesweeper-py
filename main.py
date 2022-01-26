import pygame
import sys
from board import Board
from launcher import launcher

# メインプログラム
def main():
    width, height, num_mines = launcher()       # ランチャーの起動
    board = Board(width, height, num_mines)     # ゲームの準備
    board.setup()                               # 初期設定
    board.run()                                 # ゲーム本体の起動
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()