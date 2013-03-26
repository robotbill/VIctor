import pyglet;
from itertools import chain;
from victor.vector import *;

__all__ = ['MovementGrid'];

scales = (5, 10, 25, 50, 100);

class MovementGrid(object):
    def __init__(self, width, height, color = (127, 127, 127 , 127)):  
        self.color = color;
        self.width = width;
        self.height = height;

        self.scale = 2;

        self.visible = True;
        self.batch = None;
    
    def reset_batch(self):
        batch = pyglet.graphics.Batch();
        scale = scales[self.scale];

        for i in xrange(scale, self.width, scale):
            batch.add(
                2, pyglet.gl.GL_LINES, None,
                ('v2i', (i, -scale, i, self.height + scale)),
                ('c4B', tuple(chain(self.color, self.color))),
            );

        for j in xrange(scale, self.height, scale):
            batch.add(
                2, pyglet.gl.GL_LINES, None,
                ('v2i', (-scale, j, self.width + scale, j)),
                ('c4B', tuple(chain(self.color, self.color))),
            );

        self.batch = batch;

    def draw(self):
        if self.batch and self.visible: self.batch.draw();

    def scale_up(self):
        self.scale = min(self.scale + 1, len(scales) - 1);
        self.reset_batch();

    def scale_down(self):
        self.scale = max(self.scale - 1, 0);
        self.reset_batch();

    def clamp_left_down(self, pos):
        scale = scales[self.scale];
        return scale * (pos // scale);

    def up(self, pos, multiplier=1):
        scale = scales[self.scale];
        return self.clamp_left_down(pos + vec2f(0., scale * multiplier));

    def right(self, pos, multiplier=1):
        scale = scales[self.scale];
        return self.clamp_left_down(pos + vec2f(scale * multiplier, 0));

    def left(self, pos, multiplier=1):
        scale = scales[self.scale];
        return self.clamp_left_down(pos - vec2f(.01 + scale*(multiplier - 1), 0));

    def down(self, pos, multiplier=1):
        scale = scales[self.scale];
        return self.clamp_left_down(pos - vec2f(0, .01 + scale*(multiplier - 1)));
