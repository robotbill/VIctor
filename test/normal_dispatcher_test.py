import unittest
import pyglet.window.key as pkey

import victor.normal_dispatcher as dispatcher
from victor.normal_dispatcher import *
    
class MockGrid(object):
    def __init__(self):
        self.direction = None
        self.visible = False

    def left(self, x, y): 
        return (x-1, y)

class MockCursor(object):
    def __init__(self, position=(0, 0)):
        self.position = position

class MockApp(object):
    def __init__(self):
        self.cursor = MockCursor()
        self.grid = MockGrid()
        self.marks = { };

class NormalDispatcherTest(unittest.TestCase):
    def test_move_command(self):
        app = MockApp()

        state = dispatcher.init_state(dispatcher.default_state, app, None);
        state.send((ON_KEY_PRESS, pkey.H))
        self.assertEqual(app.cursor.position, (-1, 0))

    def test_set_mark(self):
        app = MockApp();
        app.cursor.position = (314, 159);

        state = dispatcher.init_state(dispatcher.default_state, app, None);
        state.send((ON_KEY_PRESS, pkey.M));
        state.send((ON_KEY_RELEASE, pkey.M));
        state.send((ON_KEY_PRESS, pkey.B));

        app.cursor.position = (0, 0);
        self.assertEqual(app.marks['b'], (314, 159));

    def test_toggle_on(self):
        app = MockApp();

        state = dispatcher.init_state(dispatcher.default_state, app, None);
        state.send((ON_KEY_PRESS, pkey.G))
        self.assertTrue(app.grid.visible)

if __name__ == '__main__':
    unittest.main();
