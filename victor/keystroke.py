import pyglet

from victor.settings import TEXT_STYLE

class Keystrokes(object):
    def __init__(self, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument("")
        self.document.set_style(0, 0, TEXT_STYLE)

        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)

        self.layout.x = x
        self.layout.y = y
        self.layout.anchor_x = "left"
        self.layout.anchor_y = "bottom"

        self.is_clear_pending = False
        self.clear_time = 0
        self.clear_delay = 1.0

    def text(self):
        return self.document.text

    def push_text(self, text):
        if self.is_clear_pending:
            self.clear_text()
            self.is_clear_pending = False

        if text == ":":
            self.clear_text()
        else:
            self.document.text += text

    def set_clear_time(self, time):
        self.is_clear_pending = True
        self.clear_time = time + self.clear_delay

    def clear_text(self, time=None):
        if time is None:
            self.document.text = ""
        else:
            if time >= self.clear_time and self.is_clear_pending: self.document.text = ""

