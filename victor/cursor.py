import pyglet

#directions = {
#    'j' : Vector(0, -1),
#    'k' : Vector(0, 1),
#    'l' : Vector(1, 0),
#    'h' : Vector(-1, 0),
#}

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

    def move(self, match, fast=False):
        dt = 1
        mult, dir = match.group("mult"), match.group("dir")

        if mult: dt *= int(mult)

        if dir == "j": self.y -= dt
        elif dir == "k": self.y += dt
        elif dir == "h": self.x -= dt
        elif dir == "l": self.x += dt

#        self.pos += mult * directions[dir];
