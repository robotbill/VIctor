import pyglet

from villustrator.settings import TEXT_STYLE

class KeystrokeDisplay(object):
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

    def push_text(self, text):
        if text == ":":
            self.clear_text()
        else:
            self.document.text += text

    def clear_text(self, *optional_args):
        self.document.text = ""

