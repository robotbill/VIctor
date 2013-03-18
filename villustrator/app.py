import collections
import pyglet
import pyglet.window.key as pkey
import re
import sys


import villustrator.mode as vmode
from villustrator.command_area import CommandArea
from villustrator.keystroke import Keystrokes
from villustrator.command import Command
from villustrator.cursor import Cursor

NormalCommand = collections.namedtuple("NormalCommand", ["regex", "run"])

class VIllustratorApp(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(VIllustratorApp, self).__init__(640, 400, caption="VI-llustrator")

        self.mode = vmode.COMMAND

        self.batch = pyglet.graphics.Batch()
        self.command_area = CommandArea(0, 0, 550, self.batch)
        self.keystrokes = Keystrokes(550, 0, 70, self.batch)
        self.cursor = Cursor(320, 200, self.batch)

        self.keys_down = set()
        self.marks = dict()

        self.is_movement_scheduled = False
        self.frame = 0

        self.set_normal_commands()
        self.set_ex_commands()

    def set_normal_commands(self):
        self.normal_commands = [
            NormalCommand(re.compile("^m\w"), self.set_mark)
        ]

    def set_ex_commands(self):
        self.ex_commands = {
            "line": self.draw_line,
            "marks": self.show_marks
        }

    def set_mode(self, mode):
        if self.is_ex_mode():
            self.command_area.unfocus()

        self.mode = mode

        if mode == vmode.EX:
            self.command_area.focus()

    def run_command(self):
        command = Command(self.command_area.text)
        if command.command in self.ex_commands:
            self.ex_commands[command.command](*command.arguments)
        self.set_mode(vmode.COMMAND)

    def run_normal_command(self):
        if not self.keystrokes.text(): return

        for command in self.normal_commands:
            if command.regex.match(self.keystrokes.text()):
                command.run(self.keystrokes.text())
                self.keystrokes.clear_text()
                return;

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
            else:
                self.run_normal_command()

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
            #FIXME for some reason L doesn't clear these on it's own... find the real reason
            self.keystrokes.clear_text()

    def on_text(self, text):
        if self.is_ex_mode():
            self.command_area.on_text(text)
        elif self.is_command_mode():
            self.keystrokes.push_text(text)

    def on_text_motion(self, motion):
        if self.is_ex_mode():
            self.command_area.on_text_motion(motion)

    def set_mark(self, text):
        print "mark: {}".format(text[1])

        self.marks[text[1]] = (self.cursor.x, self.cursor.y)
        self.batch.add(1, pyglet.gl.GL_POINTS, None,
            ('v2i', (self.cursor.x, self.cursor.y)),
            ('c4B', (255, 0, 0, 255)))

    def draw_line(self, *args):
        if len(args) != 2:
            self.error("line requires two arguments", args)
        else:
            print(args)
            start = self.marks[args[0]]
            end = self.marks[args[1]]

            print "{}, {}".format(start, end)

            self.batch.add(2, pyglet.gl.GL_LINES, None,
                ('v2i', (start[0], start[1], end[0], end[1])),
                ('c4B', (255, 0, 0, 255, 255, 0, 0, 255)))

    def show_marks(self, *args):
        for key, value in self.marks.iteritems():
            print key, value

    def error(self, *args):
        print args

    def on_draw(self):
#        self.frame += 1
#        sys.stdout.write(" frame: %i\r" % self.frame)
#        sys.stdout.flush()

        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()

    def is_command_mode(self):
        return self.mode == vmode.COMMAND

    def is_ex_mode(self):
        return self.mode == vmode.EX
