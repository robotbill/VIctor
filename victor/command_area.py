import pyglet

import pyglet.window.key as pkey
from victor.settings import TEXT_STYLE

class CommandArea(object):
    def __init__(self, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument("")
        self.document.set_style(0, 0, TEXT_STYLE)

        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)

        self.caret = pyglet.text.caret.Caret(self.layout)

        self.has_focus = False

        self.layout.x = x
        self.layout.y = y
        self.layout.anchor_x = "left"
        self.layout.anchor_y = "bottom"

    @property
    def text(self):
        return self.document.text

    def focus(self):
        self.caret.visible = True
        self.document.text = ":"
        self.caret.position = len(self.document.text)
        self.has_focus = True

    def unfocus(self):
        self.caret.visible = False
        self.caret.position = 0
        self.document.text = ""
        self.has_focus = False

    def on_text(self, text):
        self.caret.on_text(text)

    def on_text_motion(self, motion):
        self.caret.on_text_motion(motion)

        if motion == pkey.MOTION_BACKSPACE and self.caret.position == 0:
            self.has_focus = False
