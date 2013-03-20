import collections
import pyglet
import re

__all__ = ["run_normal_command"]

NormalCommand = collections.namedtuple("NormalCommand", ["regex", "run"])

def move(app, match):
    pos = app.cursor.position;
    mult, d = match.group('mult'), match.group('dir');

    if d == "j": app.cursor.position = tuple(map(int, app.grid.down(*pos)));
    elif d == "k": app.cursor.position = tuple(map(int, app.grid.up(*pos)));
    elif d == "h": app.cursor.position = tuple(map(int, app.grid.left(*pos)));
    elif d == "l": app.cursor.position = tuple(map(int, app.grid.right(*pos)));

def set_mark(app, match):
    app.marks[match.group("id")] = app.current_position()

    app.batch.add(1, pyglet.gl.GL_POINTS, None,
        ('v2i', app.cursor.position),
        ('c4B', app.options["color"]))

def scale(app, match):
    s = match.group('scale');
    if s == 's': app.grid.scale_down();
    elif s == 'S': app.grid.scale_up();

def toggle_visible(app, match):
    app.grid.visible = not app.grid.visible;

normal_commands = [
    NormalCommand(re.compile(r"^(?P<mult>\d*)(?P<dir>(?:j|k|h|l))"), move),
    NormalCommand(re.compile(r"^m(?P<id>\w)"), set_mark),
    NormalCommand(re.compile(r"^(?P<scale>[sS])"), scale),
    NormalCommand(re.compile(r"^g"), toggle_visible),
];

def run_normal_command(app):
    if not app.keystrokes.text(): return

    for command in normal_commands:
        match = command.regex.match(app.keystrokes.text())
        if match:
            command.run(app, match)
            app.keystrokes.clear_text()
            return
