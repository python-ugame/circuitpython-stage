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
        if not 0 < self.x < 112:
            self.dx = -self.dx
        if not 0 < self.y < 112:
            self.dy = -self.dy


bank = stage.Bank.from_bmp16("ball.bmp")
background = stage.Grid(bank)
text = stage.Text(12, 1)
text.move(16, 60)
text.text("Hello world!")
ball1 = Ball(64, 0)
ball2 = Ball(0, 76)
ball3 = Ball(111, 64)
game = stage.Stage(ugame.display, 12)
sprites = [ball1, ball2, ball3]
game.layers = [text, ball1, ball2, ball3, background]
game.render_block(0, 0, 128, 128)

while True:
    for sprite in sprites:
        sprite.update()
    game.render_sprites(sprites)
    game.tick()
