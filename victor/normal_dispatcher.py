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
    time = app.time
    delta = 0.1
    fast_move_delay = 0.5

    def move_cursor(multiplier=1):
        if d == pkey.J: app.cursor.position = vec2i(*app.grid.down(pos, multiplier));
        elif d == pkey.K: app.cursor.position = vec2i(*app.grid.up(pos, multiplier));
        elif d == pkey.H: app.cursor.position = vec2i(*app.grid.left(pos, multiplier));
        elif d == pkey.L: app.cursor.position = vec2i(*app.grid.right(pos, multiplier));

    move_cursor()

    while True:
        event = yield
        if (event == NormalEvent(ON_KEY_RELEASE, d)): return
        elif (event == NormalEvent(TIMER_FIRE,)):
            if app.time - time > fast_move_delay:
                multiplier = 2 + (app.time - time - fast_move_delay)//delta
                move_cursor(multiplier)

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
    if event.modifiers & pkey.MOD_SHIFT: app.grid.scale_up()
    else: app.grid.scale_down()

def start_path(app, event):
    app.start_path();

def append_to_path(app, event):
    app.append_path();

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
		NormalEvent(ON_KEY_PRESS, pkey.B): start_path,
		NormalEvent(ON_KEY_PRESS, pkey.A): append_to_path,
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
    """
        Constructs and returns an event dispatching state machine.

        The default_state accepts a NormalEvent, looks it up then transitions
        to the state that will handle it.

        Once a "current_state" is defined the event is forwarded to it for
        handling.

        A state can be either a function that does some work then returns None
        or a function that may or may not do work, then returns a generator.
        Both should have the prototype "def state_name(app, event)." The former
        will imediately return back to the default state after doing its work.
        The latter (possibly) does work then waits for the next event.

        Typical structure of a generator returning state:

            def state(app, event):
                # do stuff
                while True:
                    event = yield;
                    # handle events
                    if is_done_handling_events_event: return

    """
    return init_state(default_state, app, None);
