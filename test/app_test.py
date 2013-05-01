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

    @patch('pyglet.window.Window.__init__')
    @patch('victor.app.VIctorApp.setup_cursor')
    def test_switch_to_ex_mode_on_key_press_then_on_text_event(self, setup_cursor, window_init):
        app = VIctorApp()
        self.assertFalse(app.is_ex_mode())
        app.on_key_press(pkey.SEMICOLON, pkey.MOD_SHIFT)
        self.assertFalse(app.is_ex_mode())
        app.on_text(':')
        self.assertTrue(app.is_ex_mode())

if __name__ == '__main__':
    unittest.main()
