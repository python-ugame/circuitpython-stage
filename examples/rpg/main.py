import random
import ugame
import stage


g = stage.Bank.from_bmp16("ground.bmp")
b = stage.Bank.from_bmp16("tiles.bmp")
l1 = stage.Grid(g)
l0 = stage.Grid(b, 10, 9)
l0.tile(0, 0, 13)
l0.move(-8, -8)
for y in range(8):
    for x in range(8):
        l1.tile(x, y, random.randint(0, 4))
for y in range(9):
    for x in range(9):
        t = 0
        bit = 1
        for dx in (0, -1):
            for dy in (-1, 0):
                if l1.tile(x + dx, y + dy) == 4:
                    t |= bit
                bit <<= 1
        l0.tile(x, y, 15 - t)
p = stage.Sprite(g, 15, 10, 10)
t = stage.Text(14, 14)
t.move(8, 8)
t.text("Hello world!")

game = stage.Stage(ugame.display, 12)
sprites = [
    stage.Sprite(g, 15, 60, 50),
    stage.Sprite(g, 15, 70, 60),
    stage.Sprite(g, 15, 80, 70),
    stage.Sprite(g, 15, 90, 80),
    stage.Sprite(g, 15, 100, 90),
    p,
]
game.layers = [t, l0] + sprites + [l1]
game.render(0, 0, 128, 128)

frame = 0
while True:
    frame = (frame + 1) % 8
    keys = ugame.buttons.get_pressed()
    if keys & ugame.K_RIGHT:
        p.move(p.x, p.y + 2)
        p.set_frame(12 + frame // 4, 0)
    elif keys & ugame.K_LEFT:
        p.move(p.x, p.y - 2)
        p.set_frame(12 + frame // 4, 4)
    elif keys & ugame.K_UP:
        p.move(p.x + 2, p.y)
        p.set_frame(14, (frame // 4) * 4)
    elif keys & ugame.K_DOWN:
        p.move(p.x - 2, p.y)
        p.set_frame(15, (frame // 4) * 4)
    else:
        p.set_frame(15, (frame // 4) * 4)
    for sprite in sprites:
        if sprite != p:
            sprite.set_frame(15, (frame // 4) * 4)
        x0 = min(sprite.px, sprite.x)
        y0 = min(sprite.py, sprite.y)
        x1 = max(sprite.px, sprite.x) + 16
        y1 = max(sprite.py, sprite.y) + 16
        game.render(x0, y0, x1, y1)
    game.tick()
