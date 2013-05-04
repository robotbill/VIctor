import collections
import pyglet
import pyglet.gl as gl
import pyglet.window.key as pkey
import re, sys, time

from itertools import chain

import victor.mode as vmode
from victor.command_area import CommandArea
from victor.cursor import Cursor
from victor.keystroke import Keystrokes
from victor.movement_grid import MovementGrid;

from victor.command import CommandException, register_ex_command, run_ex_command

from victor.path_group import PathGroup;
from victor.path import Path;

import victor.normal_dispatcher as vnd;

class VIctorApp(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(VIctorApp, self).__init__(640, 400, caption="victor")

        self.set_default_options()

        self.mode = vmode.NORMAL
        self.down_action = None
        self.text_event = None

        self.batch = pyglet.graphics.Batch()

        self.setup_cursor()

        self.marks = dict()

        self.command_area = CommandArea(0, 0, 550, self.batch)
        self.keystrokes = Keystrokes(550, 0, 70, self.batch)

        self.current_multiplier = None
        self.normal_dispatcher = vnd.construct_dispatcher(self);
        self.set_ex_commands()

        self.groups = self.current_group = PathGroup();
        self.current_path = None;

        self.time = time.time()
        pyglet.clock.schedule_interval(self.on_timer_fire, .05)

        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_BLEND)

    def setup_cursor(self):
        self.cursor = Cursor(320, 200, self.batch)
        self.grid = MovementGrid(640, 400, self.options['gridcolor']);
        self.grid.reset_batch();

    def set_ex_commands(self):
        register_ex_command('line', self.draw_line)
        register_ex_command('marks', self.show_marks)
        register_ex_command('set', self.set_option)

    def set_default_options(self):
        self.options = {}
        self.options["color"] = (0, 0, 0, 255)
        self.options["gridcolor"] = (0, 0, 255, 50)

    def set_mode(self, mode):
        if self.is_ex_mode():
            self.command_area.unfocus()

        self.mode = mode

        if mode == vmode.EX:
            self.command_area.focus()

    def switch_to_ex_mode(self):
        self.set_mode(vmode.EX)

    def run_command(self):
        try: run_ex_command(self.command_area.text)
        except CommandException as e: sys.stderr.write('%s\n' % str(e))
        self.set_mode(vmode.NORMAL)

    def on_timer_fire(self, dt):
        self.time = time.time()
        self.normal_dispatcher.send(vnd.NormalEvent(vnd.TIMER_FIRE));

    def dispatch_both(self):
        if self.down_action is None: return
        if self.text_event is None: return

        self.down_action()
        self.down_action = self.text_event = None

    def on_key_press(self, symbol, modifiers):
        is_mod_key = lambda key, mod: symbol == key and modifiers & mod

        if self.is_ex_mode() and symbol == pkey.ENTER:
            self.run_command()

        elif symbol == pkey.ESCAPE or is_mod_key(pkey.BRACKETLEFT, pkey.MOD_CTRL):
            if not self.is_normal_mode(): self.set_mode(vmode.NORMAL)
            self.keystrokes.push_text("^[")
            self.normal_dispatcher.send(vnd.NormalEvent(vnd.ESCAPE))

            # don't close window
            return pyglet.event.EVENT_HANDLED

        elif self.is_normal_mode():
            self.normal_dispatcher.send(vnd.NormalEvent(vnd.ON_KEY_PRESS, symbol, modifiers));

    def on_key_release(self, symbol, modifiers):
        if self.is_normal_mode():
            self.normal_dispatcher.send(vnd.NormalEvent(vnd.ON_KEY_RELEASE, symbol, modifiers));

    def on_text(self, text):
        if self.is_ex_mode():
            self.command_area.on_text(text)
            if not self.command_area.text:
                self.set_mode(vmode.NORMAL)
        elif self.is_normal_mode():
            if text == ':':
                self.text_event = text
                self.dispatch_both()

            self.keystrokes.push_text(text)

    def on_text_motion(self, motion):
        if self.is_ex_mode():
            self.command_area.on_text_motion(motion)

            if not self.command_area.has_focus:
                self.set_mode(vmode.NORMAL)

    def current_position(self):
        return (self.cursor.x, self.cursor.y)

    def start_path(self):
        self.current_path = Path(self.cursor.position);
        self.paths.append(self.current_path);

    def append_path(self):
        if self.current_path:
            self.current_path.append(self.cursor.position);

    def draw_line(self, *args):
        if len(args) != 2:
            self.error("line requires two arguments", args)
        else:
            start = self.marks[args[0]]
            end = self.marks[args[1]]

            self.batch.add(2, pyglet.gl.GL_LINES, None,
                ('v2i', (start[0], start[1], end[0], end[1])),
                ('c4B', tuple(chain(self.options["color"], self.options["color"]))))

    def show_marks(self, *args):
        for key, value in self.marks.iteritems():
            print key, value

    def set_option(self, *args):
        if len(args) < 2: raise CommandException("No option specified")

        option = args[0]
        if option == "color":
            if len(args) != 5: raise CommandException("color must have 4 arguments")
            self.options["color"] = tuple(map(int, args[1:]))
        elif option == "gridcolor":
            pass

    def error(self, *args):
        print args;

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.grid.draw();
        self.batch.draw()
        self.groups.draw();

    def is_normal_mode(self):
        return self.mode == vmode.NORMAL

    def is_ex_mode(self):
        return self.mode == vmode.EX
