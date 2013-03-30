from victor.path import Path;
from victor.vector import *;

__all__ = [ 'PathGroup' ];

class PathGroup(object):
    def __init__(self):
        self.transform = identity();
        self.children = [ ];
    
    def append_path(self, p):
        self.children.append(p);
        return p;

    def append_group(self):
        g = PathGroup();
        self.children.append(g);
        return g;

    def draw(self):
        for child in self.children: child.draw();
