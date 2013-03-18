import pyglet

from villustrator.app import VIllustratorApp

pyglet.resource.path = [ 'resource' ]
window = VIllustratorApp()
pyglet.app.run()
