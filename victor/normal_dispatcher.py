import pyglet.window.key as pkey;
from victor.vector import *;

__all__ = [
    'construct_dispatcher',
    'NormalEvent',
    'ON_KEY_PRESS',
    'ON_KEY_RELEASE',
    'TIMER_FIRE',
];

ON_KEY_PRESS   = 0x01;
ON_KEY_RELEASE = 0x02;
TIMER_FIRE     = 0x03;

class NormalEvent(object):
    def __init__(self, type, key=None, modifiers=0x0):
        self.type = type
        self.key = key
        self.modifiers = modifiers

    def __eq__(self, other):
        return (self.type == other.type
                and self.key == other.key
                and self.modifiers == other.modifiers)

    def __hash__(self):
        return hash((self.type, self.key, self.modifiers))


def init_state(gen, app, event):
    out = gen(app, event);

    if out is None: return None

    next(out);
    return out;

def moving(app, event):
    pos = app.cursor.position;
    d = event.key

    if d == pkey.J: app.cursor.position = vec2i(*app.grid.down(pos));
    elif d == pkey.K: app.cursor.position = vec2i(*app.grid.up(pos));
    elif d == pkey.H: app.cursor.position = vec2i(*app.grid.left(pos));
    elif d == pkey.L: app.cursor.position = vec2i(*app.grid.right(pos));

    print app.cursor.position;

    while True:
        event = yield
        if (event == NormalEvent(ON_KEY_RELEASE, d)): return
        elif (event == NormalEvent(TIMER_FIRE,)): pass

def marking(app, event):
    alphabet = map(chr, range(ord('a'), ord('z')));
    available = { getattr(pkey, ch.upper()) : ch for ch in alphabet };

    while True:
        event = yield;

        if event.type == ON_KEY_PRESS:
            if event.key in available:
                app.marks[available[event.key]] = app.cursor.position;
            return;

def toggle_grid(app, event):
    app.grid.visible = not app.grid.visible;

def scale_grid(app, event):
    if event.modifiers & pkey.MOD_SHIFT:
        app.grid.scale_up()
    else:
        app.grid.scale_down()

def default_state(app, event):
    event_map = {
        NormalEvent(ON_KEY_PRESS, pkey.J): moving,
        NormalEvent(ON_KEY_PRESS, pkey.K): moving,
        NormalEvent(ON_KEY_PRESS, pkey.H): moving,
        NormalEvent(ON_KEY_PRESS, pkey.L): moving,
        NormalEvent(ON_KEY_PRESS, pkey.M): marking,
        NormalEvent(ON_KEY_PRESS, pkey.G): toggle_grid,
        NormalEvent(ON_KEY_PRESS, pkey.S): scale_grid,
        NormalEvent(ON_KEY_PRESS, pkey.S, pkey.MOD_SHIFT): scale_grid,
    };

    current_state = None

    while True:
        event = yield

        if current_state is not None:
            try: current_state.send(event)
            except StopIteration: current_state = None
        elif event in event_map:
            current_state = init_state(event_map[event], app, event)

def construct_dispatcher(app):
    return init_state(default_state, app, None);
