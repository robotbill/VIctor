import unittest
import pyglet.window.key as pkey
from numpy.testing.utils import assert_array_equal

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

    def toggle_visibility(self):
        self.visible = not self.visible

class MockCursor(object):
    def __init__(self, position = vec2i()):
        self.position = position

class MockKeystrokes(object):
    def __init__(self):
        self.is_clear_pending = False

    def clear_text(self, *args): pass
    def set_clear_time(self, *args): pass

class MockApp(object):
    def __init__(self):
        self.cursor = MockCursor()
        self.grid = MockGrid()
        self.keystrokes = MockKeystrokes()
        self.marks = { };
        self.time = 0
        self.current_multiplier = None
        self.down_action = None
        self.dispatch_both_was_called = False

    def switch_to_ex_mode(self, on_key_press=False):
        pass

    def dispatch_both(self):
        self.dispatch_both_was_called = True

class NormalDispatcherTest(unittest.TestCase):
    def test_move_command(self):
        app = MockApp()

        state = dispatcher.init_state(dispatcher.default_state, app, None);
        state.send(NormalEvent(ON_KEY_PRESS, pkey.H))
        assert_array_equal(app.cursor.position, vec2i(-1, 0))

    def test_fast_move(self):
        app = MockApp()
        app.time = 0

        state = dispatcher.init_state(dispatcher.default_state, app, None)
        state.send(NormalEvent(ON_KEY_PRESS, pkey.H))
        assert_array_equal(app.cursor.position, vec2i(-1, 0))

        app.time = 0.498
        state.send(NormalEvent(TIMER_FIRE));
        assert_array_equal(app.cursor.position, vec2i(-1, 0))

        app.time = 0.51
        state.send(NormalEvent(TIMER_FIRE));
        assert_array_equal(app.cursor.position, vec2i(-2, 0))

        app.time = 0.71
        state.send(NormalEvent(TIMER_FIRE));
        assert_array_equal(app.cursor.position, vec2i(-6, 0))

        app.time = 0.81
        state.send(NormalEvent(TIMER_FIRE));
        assert_array_equal(app.cursor.position, vec2i(-11, 0))

    def test_fast_move_doesnt_keep_moving_after_key_release(self):
        app = MockApp()
        app.time = 0

        state = dispatcher.init_state(dispatcher.default_state, app, None)
        state.send(NormalEvent(ON_KEY_PRESS, pkey.H))
        assert_array_equal(app.cursor.position, vec2i(-1, 0))

        state.send(NormalEvent(ON_KEY_RELEASE, pkey.H))

        app.time = 0.71
        state.send(NormalEvent(TIMER_FIRE));
        assert_array_equal(app.cursor.position, vec2i(-1, 0))

    def test_multipliers(self):
        app = MockApp()

        state = dispatcher.init_state(dispatcher.default_state, app, None)
        state.send(NormalEvent(ON_KEY_PRESS, pkey._1))
        state.send(NormalEvent(ON_KEY_PRESS, pkey._0))
        state.send(NormalEvent(ON_KEY_PRESS, pkey.H))
        assert_array_equal(app.cursor.position, vec2i(-10, 0))

    def test_multipliers_fast_move_starts_at_jump(self):
        app = MockApp()
        app.time = 0

        state = dispatcher.init_state(dispatcher.default_state, app, None)
        state.send(NormalEvent(ON_KEY_PRESS, pkey._2))
        state.send(NormalEvent(ON_KEY_PRESS, pkey.H))
        assert_array_equal(app.cursor.position, vec2i(-2, 0))

        app.time = 0.51
        state.send(NormalEvent(TIMER_FIRE))
        assert_array_equal(app.cursor.position, vec2i(-3, 0))

        app.time = 0.61
        state.send(NormalEvent(TIMER_FIRE))
        assert_array_equal(app.cursor.position, vec2i(-4, 0))


    def test_set_mark(self):
        app = MockApp();
        app.cursor.position = vec2i(314, 159);

        state = dispatcher.init_state(dispatcher.default_state, app, None);
        state.send(NormalEvent(ON_KEY_PRESS, pkey.M));
        state.send(NormalEvent(ON_KEY_RELEASE, pkey.M));
        state.send(NormalEvent(ON_KEY_PRESS, pkey.B));

        app.cursor.position = vec2i(0, 0);
        assert_array_equal(app.marks['b'], vec2i(314, 159))

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

    def test_switch_to_ex_mode(self):
        app = MockApp()
        state = dispatcher.init_state(dispatcher.default_state, app, None)
        state.send(NormalEvent(ON_KEY_PRESS, pkey.COLON))
        self.assertEqual(app.down_action, app.switch_to_ex_mode)
        self.assertTrue(app.dispatch_both_was_called)

    def test_switch_to_ex_mode__semi_colon_and_shift(self):
        app = MockApp()
        state = dispatcher.init_state(dispatcher.default_state, app, None)
        state.send(NormalEvent(ON_KEY_PRESS, pkey.SEMICOLON, pkey.MOD_SHIFT))
        self.assertEqual(app.down_action, app.switch_to_ex_mode)
        self.assertTrue(app.dispatch_both_was_called)

    def test_instantiating_normal_event_strips_num_lock_modifier(self):
        event = NormalEvent(ON_KEY_PRESS, pkey.A, pkey.MOD_NUMLOCK)
        self.assertFalse(event.modifiers)

    def test_certain_modifier_key_presses_do_not_change_state(self):
        app = MockApp()
        state = dispatcher.init_state(dispatcher.default_state, app, None)
        state.send(NormalEvent(ON_KEY_PRESS, pkey.M))
        current_state = state.gi_frame.f_locals['current_state']
        self.assertEqual(current_state.__name__, 'marking')

        keys = [
            pkey.LSHIFT, pkey.RSHIFT,
            pkey.LCTRL, pkey.RCTRL,
            pkey.CAPSLOCK,
            pkey.LMETA, pkey.RMETA,
            pkey.LALT, pkey.RALT,
            pkey.LWINDOWS, pkey.RWINDOWS,
            pkey.LCOMMAND, pkey.RCOMMAND,
            pkey.LOPTION, pkey.ROPTION
        ]

        for key in keys:
            state.send(NormalEvent(ON_KEY_PRESS, key))
            current_state = state.gi_frame.f_locals['current_state']
            self.assertIsNotNone(current_state,
                    msg="{} has changed the state".format(pkey.symbol_string(key)))
            self.assertEqual(current_state.__name__, 'marking',
                    msg="current_state was changed by {}".format(pkey.symbol_string(key)))

if __name__ == '__main__':
    unittest.main();
