import collections
import pyglet
import re

__all__ = ["run_normal_command"]

NormalCommand = collections.namedtuple("NormalCommand", ["regex", "run"])

def move(app, match):
    app.cursor.move(match)

def set_mark(app, match):
    app.marks[match.group("id")] = app.current_position()

    app.batch.add(1, pyglet.gl.GL_POINTS, None,
        ('v2i', app.current_position()),
        ('c4B', (255, 0, 0, 255)))

normal_commands = [
    NormalCommand(re.compile(r"^(?P<mult>\d*)(?P<dir>(?:j|k|h|l))"), move),
    NormalCommand(re.compile(r"^m(?P<id>\w)"), set_mark)
]

def run_normal_command(app):
    if not app.keystrokes.text(): return

    for command in normal_commands:
        match = command.regex.match(app.keystrokes.text())
        if match:
            command.run(app, match)
            app.keystrokes.clear_text()
            return
