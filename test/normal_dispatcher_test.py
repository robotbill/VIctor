import unittest
import pyglet.window.key as pkey

from victor.normal_dispatcher import *
	
class MockCursor(object):
	def __init__(self, position=(0, 0)):
		self.position = position

class MockApp(object):
	def __init__(self):
		self.cursor = MockCursor()

class NormalDispatcherTest(unittest.TestCase):
	def test_move_command(self):
		app = MockApp()

		state = init_state(default_state, app, None);
		state.send((ON_KEY_PRESS, pkey.H))
		self.assertEqual(app.cursor.position, (-1, 0))

if __name__ == '__main__':
	unittest.main();
