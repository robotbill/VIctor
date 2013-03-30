import pyglet;
from victor.vector import *;

__all__ = [ 'Path' ];

def _pairwise(seq):
    from itertools import tee, izip;
    a, b = tee(iter(seq)); 
    next(b);
    return izip(a, b);

class Path(object):
    def __init__(self, pos, color = (0, 0, 0, 255)):
        self.points = [ (0., pos) ];
        self.color = color;
        self.batch = None;
    
    def append(self, p):
        self.points.append((self.points[-1][0] + 1., p));
        self.reset_batch();
    
    def evaluate(self, t):
        for p, n in _pairwise(self.points):
            if p[0] <= t < n[0]:
                return (1. - t) * p[1]  + t * p[1];
    
    def approximate(self):
        return [ vec2i(*p) for t, p in self.points ];

    def reset_batch(self):
        from itertools import islice, cycle, chain;

        batch = pyglet.graphics.Batch();
        points = self.approximate();

        batch.add(
            len(points), pyglet.gl.GL_LINE_STRIP, None,
            ('v2i', tuple(chain(*points))),
            ('c4B', tuple(islice(cycle(self.color), 0, len(self.color) * len(points))))
        );

        self.batch = batch;

    def draw(self, batch = None):
        if self.batch: self.batch.draw();
