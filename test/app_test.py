import unittest
import pyglet.window.key as pkey
from mock import patch

from victor.app import VIctorApp
import victor.mode as vmode

class AppTest(unittest.TestCase):

    @patch('pyglet.window.Window.__init__')
    @patch('victor.app.VIctorApp.setup_cursor')
    def test_switch_to_ex_mode_on_text_then_on_key_press_event(self, setup_cursor, window_init):
        app = VIctorApp()
        self.assertFalse(app.is_ex_mode())

        app.on_text(':')
        self.assertFalse(app.is_ex_mode())

        app.on_key_press(pkey.SEMICOLON, pkey.MOD_SHIFT)
        self.assertTrue(app.is_ex_mode())
        self.assertEqual(app.command_area.text, ':')

    @patch('pyglet.window.Window.__init__')
    @patch('victor.app.VIctorApp.setup_cursor')
    def test_switch_to_ex_mode_on_key_press_then_on_text_event(self, setup_cursor, window_init):
        app = VIctorApp()
        self.assertFalse(app.is_ex_mode())

        app.on_key_press(pkey.SEMICOLON, pkey.MOD_SHIFT)
        self.assertFalse(app.is_ex_mode())

        app.on_text(':')
        self.assertTrue(app.is_ex_mode())
        self.assertEqual(app.command_area.text, ':')

    @patch('pyglet.window.Window.__init__')
    @patch('victor.app.VIctorApp.setup_cursor')
    def test_switch_back_to_normal_mode_when_leading_colon_is_deleted(
        self, setup_cursor, window_init
    ):
        app = VIctorApp()
        app.switch_to_ex_mode()
        self.assertTrue(app.is_ex_mode())

        app.on_text_motion(pkey.MOTION_BACKSPACE)
        self.assertTrue(app.is_normal_mode())

    @patch('pyglet.window.Window.__init__')
    @patch('victor.app.VIctorApp.setup_cursor')
    def test_escape_switches_to_normal_mode_from_ex_mode(self, setup_cursor, window_init):
        app = VIctorApp()
        app.switch_to_ex_mode()
        self.assertTrue(app.is_ex_mode())

        app.on_key_press(pkey.ESCAPE, 0x0)
        self.assertTrue(app.is_normal_mode())

    @patch('pyglet.window.Window.__init__')
    @patch('victor.app.VIctorApp.setup_cursor')
    def test_ctrl_left_bracket_switches_to_normal_mode_from_ex_mode(self, setup_cursor, window_init):
        app = VIctorApp()
        app.switch_to_ex_mode()
        self.assertTrue(app.is_ex_mode())

        app.on_key_press(pkey.BRACKETLEFT, pkey.MOD_CTRL)
        self.assertTrue(app.is_normal_mode())

if __name__ == '__main__':
    unittest.main()
