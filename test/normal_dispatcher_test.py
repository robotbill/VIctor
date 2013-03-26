import unittest
import pyglet.window.key as pkey

import victor.normal_dispatcher as dispatcher
from victor.normal_dispatcher import *
from victor.vector import *;
    
class MockGrid(object):
    def __init__(self):
        self.visible = False
        self.scale = 1

    def left(self, pos, multiplier):
        return pos - vec2i(1 * multiplier, 0);

    def scale_down(self):
        self.scale -= 1

    def scale_up(self):
        self.scale += 1

class MockCursor(object):
    def __init__(self, position = vec2i()):
        self.position = position

class MockApp(object):
    def __init__(self):
        self.cursor = MockCursor()
        self.grid = MockGrid()
        self.marks = { };
        self.time = 0

class NormalDispatcherTest(unittest.TestCase):
    def test_move_command(self):
        app = MockApp()

        state = dispatcher.init_state(dispatcher.default_state, app, None);
        state.send(NormalEvent(ON_KEY_PRESS, pkey.H))
        self.assertTrue(all(app.cursor.position == vec2i(-1, 0)))

    def test_fast_move(self):
        app = MockApp()
        app.time = 0

        state = dispatcher.init_state(dispatcher.default_state, app, None);
        state.send(NormalEvent(ON_KEY_PRESS, pkey.H))
        self.assertTrue(all(app.cursor.position == vec2i(-1, 0)))

        app.time = 0.498
        state.send(NormalEvent(TIMER_FIRE));
        self.assertTrue(all(app.cursor.position == vec2i(-1, 0)))

        app.time = 0.51
        state.send(NormalEvent(TIMER_FIRE));
        self.assertTrue(all(app.cursor.position == vec2i(-2, 0)))

        app.time = 0.71
        state.send(NormalEvent(TIMER_FIRE));
        self.assertTrue(all(app.cursor.position == vec2i(-4, 0)))

    def test_fast_move_doesnt_keep_moving_after_key_release(self):
        app = MockApp()
        app.time = 0

        state = dispatcher.init_state(dispatcher.default_state, app, None);
        state.send(NormalEvent(ON_KEY_PRESS, pkey.H))
        self.assertTrue(all(app.cursor.position == vec2i(-1, 0)))

        state.send(NormalEvent(ON_KEY_RELEASE, pkey.H))

        app.time = 0.71
        state.send(NormalEvent(TIMER_FIRE));
        self.assertTrue(all(app.cursor.position == vec2i(-1, 0)))


    def test_set_mark(self):
        app = MockApp();
        app.cursor.position = vec2i(314, 159);

        state = dispatcher.init_state(dispatcher.default_state, app, None);
        state.send(NormalEvent(ON_KEY_PRESS, pkey.M));
        state.send(NormalEvent(ON_KEY_RELEASE, pkey.M));
        state.send(NormalEvent(ON_KEY_PRESS, pkey.B));

        app.cursor.position = vec2i(0, 0);
        self.assertTrue(all(app.marks['b'] == vec2i(314, 159)));

    def test_toggle_on(self):
        app = MockApp();

        state = dispatcher.init_state(dispatcher.default_state, app, None);
        state.send(NormalEvent(ON_KEY_PRESS, pkey.G))
        self.assertTrue(app.grid.visible)

    def test_scale_up(self):
        app = MockApp();
        state = dispatcher.init_state(dispatcher.default_state, app, None);
        state.send(NormalEvent(ON_KEY_PRESS, pkey.S))
        self.assertEqual(app.grid.scale, 0)

    def test_scale_down(self):
        app = MockApp();
        state = dispatcher.init_state(dispatcher.default_state, app, None);
        state.send(NormalEvent(ON_KEY_PRESS, pkey.S, pkey.MOD_SHIFT))
        self.assertEqual(app.grid.scale, 2)

if __name__ == '__main__':
    unittest.main();
