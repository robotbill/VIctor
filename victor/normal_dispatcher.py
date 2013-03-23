import pyglet.window.key as pkey;

ON_KEY_PRESS   = 0x01;
ON_KEY_RELEASE = 0x02;
TIMER_FIRE     = 0x03;

def init_state(gen, app, event):
    out = gen(app, event);
    next(out);
    return out;

def moving_left(app, event):
    app.cursor.position = (app.cursor.position[0] - 1, app.cursor.position[1])

    while True:
        event = yield
        if (event == (ON_KEY_RELEASE, pkey.H)): return
        elif (event == (TIMER_FIRE,)): pass

def default_state(app, event):
    #initialize stuff

    current_state = None

    while True:
        event = yield
    
        if current_state is not None:
            try: current_state.send(app, event)
            except StopIteration: current_state = None
        elif (event == (ON_KEY_PRESS, pkey.H)):
            init_state(moving_left, app, event);
    
class NormalDispatcher(object):
    def __init__(self, app):
        self.app = app;
        self.current_state = default_state;
    
    def transition(self, event):
        self.current_state = self.current_state(app, event);
