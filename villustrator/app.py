import pyglet
import pyglet.window.key as pkey


import villustrator.mode as vmode
from villustrator.command_area import CommandArea
from villustrator.keystroke_display import KeystrokeDisplay
from villustrator.command import Command

class VIllustratorApp(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(VIllustratorApp, self).__init__(640, 400, caption="VI-llustrator")

        self.mode = vmode.COMMAND

        self.batch = pyglet.graphics.Batch()
        self.command_area = CommandArea(0, 0, 550, self.batch)
        self.keystrokes = KeystrokeDisplay(550, 0, 70, self.batch)

    def set_mode(self, mode):
        if self.is_ex_mode():
            self.command_area.unfocus()

        self.mode = mode

        if mode == vmode.EX:
            self.command_area.focus()

    def run_command(self):
        command = Command(self.command_area.text)
        command.run()
        self.set_mode(vmode.COMMAND)

    def on_key_press(self, symbol, modifiers):
        is_mod_key = lambda key, mod: symbol == key and modifiers & mod

        if self.is_ex_mode() and symbol == pkey.ENTER:
            self.run_command()

        elif self.is_command_mode() and is_mod_key(pkey.SEMICOLON, pkey.MOD_SHIFT):
            self.set_mode(vmode.EX)

        elif symbol == pkey.ESCAPE or is_mod_key(pkey.BRACKETLEFT, pkey.MOD_CTRL):
            if not self.is_command_mode(): self.set_mode(vmode.COMMAND)
            self.keystrokes.push_text("^[")
            pyglet.clock.schedule_once(self.keystrokes.clear_text, 1.0)
            return pyglet.event.EVENT_HANDLED

    def on_text(self, text):
        if self.is_ex_mode():
            self.command_area.on_text(text)
        elif self.is_command_mode():
            self.keystrokes.push_text(text)

    def on_text_motion(self, motion):
        if self.is_ex_mode():
            self.command_area.on_text_motion(motion)

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()

    def is_command_mode(self):
        return self.mode == vmode.COMMAND

    def is_ex_mode(self):
        return self.mode == vmode.EX
