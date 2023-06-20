import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}


def judge_bound(rct: pg.Rect) -> tuple[bool, bool]:

    """
    こうかとんRect、爆弾Rectが画面外かを判定する関数
    引数：こうかとんRect or 爆弾Rect
    戻り値：横方向と縦王侯のタプル (True:画面内/False:画面外)
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img_rev = pg.transform.flip(kk_img, True, False)
    kk_img_gameover = pg.image.load("ex02/fig/8.png")
    kk_img_gameover = pg.transform.rotozoom(kk_img_gameover, 0, 2.0)
    kk_img_rev = pg.transform.flip(kk_img, True, False)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    # 移動量の合計値をキーとし、rotozoomしたSurfaceを値とした辞書
    kk_direction = {
        (0, 0): pg.transform.rotozoom(kk_img, 0, 2.0),
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 2.0),
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 2.0),
        (0, -5): pg.transform.rotozoom(kk_img_rev, 90, 2.0),
        (+5, -5): pg.transform.rotozoom(kk_img_rev, 45, 2.0),
        (+5, 0): pg.transform.rotozoom(kk_img_rev, 0, 2.0),
        (+5, +5): pg.transform.rotozoom(kk_img_rev, -45, 2.0),
        (0, +5): pg.transform.rotozoom(kk_img_rev, -90, 2.0),
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 2.0),
    }

    bd_img = pg.Surface((20, 20))  
    bd_img.set_colorkey((0, 0, 0))  
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    bd_rct = bd_img.get_rect()
    bd_rct.center = x, y 
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        # ゲームオーバー時の処理
        if kk_rct.colliderect(bd_rct):
            screen.blit(bg_img, [0, 0])
            screen.blit(kk_img_gameover, kk_rct)
            screen.blit(bd_img, bd_rct)
            pg.display.update()
            pg.time.delay(2000)
            return 
        screen.blit(bg_img, [0, 0])

        # 押下キーに応じてこうかとんを移動させる
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0] # 合計移動量
        for k, mv in delta.items():
            if key_lst[k]: 
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)

        # こうかとんの画面外判定
        if judge_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_direction[tuple(sum_mv)], kk_rct)

        # 爆弾の跳ね返り処理
        judge_bd = judge_bound(bd_rct)
        if not judge_bd[0]: # もし横方向に画面外だったら
            vx *= -1
        if not judge_bd[1]: # もし縦方向に画面外だったら
            vy *= -1 

        bd_rct.move_ip(vx, vy)
        screen.blit(bd_img, bd_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()