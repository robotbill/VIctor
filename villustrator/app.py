import pyglet
import pyglet.window.key as pkey
import sys


import villustrator.mode as vmode
from villustrator.command_area import CommandArea
from villustrator.keystroke_display import KeystrokeDisplay
from villustrator.command import Command
from villustrator.cursor import Cursor

class VIllustratorApp(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(VIllustratorApp, self).__init__(640, 400, caption="VI-llustrator")

        self.mode = vmode.COMMAND

        self.batch = pyglet.graphics.Batch()
        self.command_area = CommandArea(0, 0, 550, self.batch)
        self.keystrokes = KeystrokeDisplay(550, 0, 70, self.batch)
        self.cursor = Cursor(320, 200, self.batch)

        self.keys_down = set()
        self.is_movement_scheduled = False
        self.frame = 0

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

        elif self.is_command_mode():
            if symbol == pkey.J:
                self.move("down");
            elif symbol == pkey.K:
                self.move("up");
            elif symbol == pkey.H:
                self.move("left");
            elif symbol == pkey.L:
                self.move("right");

        self.keys_down.add(symbol)

    def move(self, direction):
        if direction == "up":
            self.cursor.move_up()
        elif direction == "down":
            self.cursor.move_down()
        elif direction == "left":
            self.cursor.move_left()
        elif direction == "right":
            self.cursor.move_right()

        self.schedule_movement_clock()
        self.keystrokes.clear_text()

    def schedule_movement_clock(self, dt=0.5):
        if not self.is_movement_scheduled:
            self.is_movement_scheduled = True
            pyglet.clock.schedule_interval(self.movement, dt)

    def stop_movement_schedule(self):
        if self.is_movement_scheduled:
            self.is_movement_scheduled = False
            pyglet.clock.unschedule(self.movement)

    def on_key_release(self, symbol, modifiers):
        if symbol in self.keys_down:
            self.keys_down.remove(symbol)
        self.stop_movement_schedule()

    def movement(self, dt):
        self.stop_movement_schedule()
        self.schedule_movement_clock(0.05)

        if pkey.J in self.keys_down:
            self.cursor.move_down_fast()
        elif pkey.K in self.keys_down:
            self.cursor.move_up_fast()
        elif pkey.H in self.keys_down:
            self.cursor.move_left_fast()
        elif pkey.L in self.keys_down:
            self.cursor.move_right_fast()

    def on_text(self, text):
        if self.is_ex_mode():
            self.command_area.on_text(text)
        elif self.is_command_mode():
            self.keystrokes.push_text(text)

    def on_text_motion(self, motion):
        if self.is_ex_mode():
            self.command_area.on_text_motion(motion)

    def on_draw(self):
        self.frame += 1
        sys.stdout.write(" frame: %i\r" % self.frame)
        sys.stdout.flush()

        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()

    def is_command_mode(self):
        return self.mode == vmode.COMMAND

    def is_ex_mode(self):
        return self.mode == vmode.EX
