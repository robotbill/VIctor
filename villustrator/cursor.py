import pyglet

class Cursor(pyglet.sprite.Sprite):
    def __init__(self, x, y, batch):
        image = pyglet.resource.image("cursor_arrow.png")
        super(Cursor, self).__init__(image, x=x, y=y, batch=batch)
        self.scale = 0.3

    def move_down(self): self.y -= 1
    def move_up(self): self.y += 1
    def move_left(self): self.x -= 1
    def move_right(self): self.x += 1

    def move_down_fast(self): self.y -= 5
    def move_up_fast(self): self.y += 5
    def move_left_fast(self): self.x -= 5
    def move_right_fast(self): self.x += 5
