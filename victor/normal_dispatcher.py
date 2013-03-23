import pyglet.window.key as pkey;

ON_KEY_PRESS   = 0x01;
ON_KEY_RELEASE = 0x02;
TIMER_FIRE     = 0x03;

def init_state(gen, app, event):
    out = gen(app, event);
    next(out);
    return out;

def moving(app, event):
    pos = app.cursor.position;
    d = event[1]

    if d == pkey.J: app.cursor.position = tuple(map(int, app.grid.down(*pos)));
    elif d == pkey.K: app.cursor.position = tuple(map(int, app.grid.up(*pos)));
    elif d == pkey.H: app.cursor.position = tuple(map(int, app.grid.left(*pos)));
    elif d == pkey.L: app.cursor.position = tuple(map(int, app.grid.right(*pos)));

    while True:
        event = yield
        if (event == (ON_KEY_RELEASE, pkey.H)): return
        elif (event == (TIMER_FIRE,)): pass

def marking(app, event):
    alphabet = map(chr, range(ord('a'), ord('z')));
    available = { getattr(pkey, ch.upper()) : ch for ch in alphabet };

    while True:
        event = yield;

        if event[0] == ON_KEY_PRESS:
            if event[1] in available:
                app.marks[available[event[1]]] = app.cursor.position;
            return;

def default_state(app, event):
    event_map = {
        (ON_KEY_PRESS, pkey.J): moving,
        (ON_KEY_PRESS, pkey.K): moving,
        (ON_KEY_PRESS, pkey.H): moving,
        (ON_KEY_PRESS, pkey.L): moving,
        (ON_KEY_PRESS, pkey.M): marking,
    };

    current_state = None

    while True:
        event = yield
    
        if current_state is not None:
            try: current_state.send(event)
            except StopIteration: current_state = None
        elif event in event_map:
            current_state = init_state(event_map[event], app, event)
    
class NormalDispatcher(object):
    def __init__(self, app):
        self.app = app;
        self.current_state = default_state;
    
    def transition(self, event):
        self.current_state = self.current_state(app, event);
