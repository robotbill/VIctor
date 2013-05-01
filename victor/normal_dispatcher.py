import pyglet.window.key as pkey;

from victor.vector import *;
from victor import path;

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
ESCAPE         = 0x04;

class NormalEvent(object):
    def __init__(self, type, key=None, modifiers=0x0):
        self.type = type
        self.key = key
        self.modifiers = modifiers

        self._strip_unwanted_modifiers()

    def _strip_unwanted_modifiers(self):
        if self.modifiers:
            self.modifiers &= ~pkey.MOD_NUMLOCK

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
    jump = app.current_multiplier or 1

    def move_cursor(multiplier=1):
        if d == pkey.J: app.cursor.position = vec2i(*app.grid.down(pos, multiplier));
        elif d == pkey.K: app.cursor.position = vec2i(*app.grid.up(pos, multiplier));
        elif d == pkey.H: app.cursor.position = vec2i(*app.grid.left(pos, multiplier));
        elif d == pkey.L: app.cursor.position = vec2i(*app.grid.right(pos, multiplier));

    move_cursor(jump)
    jump += 1

    while True:
        event = yield
        if (event == NormalEvent(ON_KEY_RELEASE, d)): return
        elif (event == NormalEvent(TIMER_FIRE,)):
            if app.time - time > fast_move_delay:
                multiplier = jump + pow(((app.time - time - fast_move_delay)//delta), 2)
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
    app.grid.toggle_visibility()

def scale_grid(app, event):
    if event.modifiers & pkey.MOD_SHIFT: app.grid.scale_up()
    else: app.grid.scale_down()

def start_path(app, event):
    p = path.Path(app.cursor.position, app.options['color']);
    app.current_path = app.current_group.append_path(p);

def append_path(app, event):
    if app.current_path:
        app.current_path.append(app.cursor.position);

def switch_to_ex_mode(app, event):
    app.down_action = app.switch_to_ex_mode
    app.dispatch_both()

digit_keys = {
    pkey._0: 0,
    pkey._1: 1,
    pkey._2: 2,
    pkey._3: 3,
    pkey._4: 4,
    pkey._5: 5,
    pkey._6: 6,
    pkey._7: 7,
    pkey._8: 8,
    pkey._9: 9,
    pkey.NUM_0: 0,
    pkey.NUM_1: 1,
    pkey.NUM_2: 2,
    pkey.NUM_3: 3,
    pkey.NUM_4: 4,
    pkey.NUM_5: 5,
    pkey.NUM_6: 6,
    pkey.NUM_7: 7,
    pkey.NUM_8: 8,
    pkey.NUM_9: 9
}

modifier_keys = [
    pkey.LSHIFT,
    pkey.RSHIFT,
    pkey.LCTRL,
    pkey.RCTRL,
    pkey.CAPSLOCK,
    pkey.LMETA,
    pkey.RMETA,
    pkey.LALT,
    pkey.RALT,
    pkey.LWINDOWS,
    pkey.RWINDOWS,
    pkey.LCOMMAND,
    pkey.RCOMMAND,
    pkey.LOPTION,
    pkey.ROPTION
]

def is_digit_keypress_event(event):
    return (event.type == ON_KEY_PRESS and event.key in digit_keys
            and not event.modifiers)

def default_state(app, event):
    event_map = {
        NormalEvent(ON_KEY_PRESS, pkey.A): append_path,
        NormalEvent(ON_KEY_PRESS, pkey.B): start_path,
        NormalEvent(ON_KEY_PRESS, pkey.COLON): switch_to_ex_mode,
        NormalEvent(ON_KEY_PRESS, pkey.G): toggle_grid,
        NormalEvent(ON_KEY_PRESS, pkey.H): moving,
        NormalEvent(ON_KEY_PRESS, pkey.J): moving,
        NormalEvent(ON_KEY_PRESS, pkey.K): moving,
        NormalEvent(ON_KEY_PRESS, pkey.L): moving,
        NormalEvent(ON_KEY_PRESS, pkey.M): marking,
        NormalEvent(ON_KEY_PRESS, pkey.S): scale_grid,
        NormalEvent(ON_KEY_PRESS, pkey.S, pkey.MOD_SHIFT): scale_grid,
        NormalEvent(ON_KEY_PRESS, pkey.SEMICOLON, pkey.MOD_SHIFT): switch_to_ex_mode,
    };

    current_state = None

    def reset():
        current_state = None
        app.keystrokes.set_clear_time(app.time)

    while True:
        event = yield

        if event == NormalEvent(ESCAPE):
            reset()
            app.current_multiplier = None

        elif event.key in modifier_keys:
            continue

        elif current_state is not None:
            try:
                current_state.send(event)
            except StopIteration:
                current_state = None
                app.keystrokes.set_clear_time(app.time)
            else:
                app.keystrokes.is_clear_pending = False

        elif event in event_map:
            reset()
            current_state = init_state(event_map[event], app, event)
            app.current_multiplier = None

        elif is_digit_keypress_event(event):
            if not app.current_multiplier: app.current_multiplier = 0
            else: app.current_multiplier *= 10
            app.current_multiplier += digit_keys[event.key]

        elif event.type is ON_KEY_PRESS:
            reset()
            app.current_multiplier = None

        app.keystrokes.clear_text(app.time)

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
