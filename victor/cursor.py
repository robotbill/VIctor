import pyglet

class Cursor(pyglet.sprite.Sprite):
    def __init__(self, x, y, batch):
        image = pyglet.resource.image("cursor.png")
        image.anchor_x = image.width//2 + 1
        image.anchor_y = image.height//2

        super(Cursor, self).__init__(image, x=x, y=y, batch=batch)

    def get_position(self): return (self.x, self.y);
    def set_position(self, p): self.x, self.y = p;

    position = property(get_position, set_position);
