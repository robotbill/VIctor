import pyglet

from villustrator.command_area import CommandArea
from villustrator.keystroke_display import KeystrokeDisplay
from villustrator.command import Command

class VIllustratorApp(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(VIllustratorApp, self).__init__(640, 400, caption="VI-llustrator")

        self.focus = None

        self.batch = pyglet.graphics.Batch()
        self.command_area = CommandArea(0, 0, 600, self.batch)
        self.keystrokes = KeystrokeDisplay(600, 0, 40, self.batch)

    def set_focus(self, focus):
        if self.focus:
            self.focus.unfocus()

        self.focus = focus

        if focus:
            focus.focus()

    def run_command(self):
        command = Command(self.focus.text)
        command.run()
        self.set_focus(None)

    def on_key_press(self, symbol, modifiers):
        if self.focus == self.command_area:
            if self.focus and symbol == pyglet.window.key.ENTER:
                self.run_command()
        elif symbol == pyglet.window.key.SEMICOLON and modifiers & pyglet.window.key.MOD_SHIFT:
                self.set_focus(self.command_area)
        elif symbol == pyglet.window.key.ESCAPE:
            if self.focus: set_focus(None)
            self.keystrokes.push_text("^[")
            pyglet.clock.schedule_once(self.keystrokes.clear_text, 1.0)
            return pyglet.event.EVENT_HANDLED

    def on_text(self, text):
        if self.focus:
            self.focus.on_text(text)
        else:
            self.keystrokes.push_text(text)

    def on_text_motion(self, motion):
        if self.focus:
            self.focus.on_text_motion(motion)

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()
