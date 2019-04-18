import ugame
import stage


class Ball(stage.Sprite):
    def __init__(self, x, y):
        super().__init__(bank, 1, x, y)
        self.dx = 2
        self.dy = 1

    def update(self):
        super().update()
        self.set_frame(self.frame % 4 + 1)
        self.move(self.x + self.dx, self.y + self.dy)
        if not 0 < self.x < (ugame.display.width - 16):
            self.dx = -self.dx
        if not 0 < self.y < (ugame.display.height - 16):
            self.dy = -self.dy


bank = stage.Bank.from_bmp16("ball.bmp")
background = stage.Grid(bank, (ugame.display.width//16), (ugame.display.height//16))
text = stage.Text(12, 1)
text.move(16, (ugame.display.height//2 - 4))
text.text("Hello world!")
ball1 = Ball((ugame.display.width//2), 0)
ball2 = Ball(0, (ugame.display.height//2))
ball3 = Ball((ugame.display.width//6*2), 16)
game = stage.Stage(ugame.display, 12)
sprites = [ball1, ball2, ball3]
game.layers = [text, ball1, ball2, ball3, background]
game.render_block(0, 0, (ugame.display.width), (ugame.display.height))


while True:
    for sprite in sprites:
        sprite.update()
    game.render_sprites(sprites)
    game.tick()
