import numpy as np;

__all__ = [
    'vec2i', 'vec2f',
    'vec3i', 'vec3f',
    'vec4i', 'vec4f',
    'matrix2f', 'matrix2i',
    'matrix3f', 'matrix3i',
    'matrix4f', 'matrix4i',
    'identity', 'translate', 'scale',
];

def vec2i(x = 0, y = 0):
    return np.array([x, y], dtype = np.int32);

def vec2f(x  = 0., y = 0.):
    return np.array([x, y], dtype = np.float32);

def vec3i(x = 0, y = 0, z = 0):
    return np.array([x, y, z], dtype = np.int32);

def vec3f(x = 0, y = 0., z = 0.):
    return np.array([x, y, z], dtype = np.float32);

def vec4i(x = 0, y = 0, z = 0,  w = 0):
    return np.array([x, y, z, w], dtype = np.int32);

def vec4f(x = 0., y = 0., z = 0., w = 0.):
    return np.array([x, y, z, w], dtype = np.float32);

def matrix2f(r1, r2):
    return np.array([ r1, r2 ], dtype = np.float32);

def matrix2i(r1, r2):
    return np.array([ r1, r2 ], dtype = np.int32);

def matrix3f(r1, r2, r3):
    return np.array([ r1, r2, r3 ], dtype = np.float32);

def matrix3i(r1, r2, r3):
    return np.array([ r1, r2, r3 ], dtype = np.int32);

def matrix4f(r1, r2, r3, r4):
    return np.array([ r1, r2, r3, r4 ], dtype = np.float32);

def matrix4i(r1, r2, r3, r4):
    return np.array([r1, r2, r3, r4 ], dtype = np.int32);

def identity():
    return matrix3f([ 1, 0, 0 ], [ 0, 1, 0 ], [ 0, 0, 1 ]);

def translate(x, y):
    return matrix3f([ 1, 0, 0 ], [ 0, 1, 0 ], [ x, y, 1 ])

def scale(x, y):
    return matrix3f([ x, 0, 0 ], [ 0, y, 0 ], [ 0, 0, 1 ]);
