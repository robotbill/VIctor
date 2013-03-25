import numpy as np;

__all__ = [
    'vec2i', 'vec2f',
    'vec3i', 'vec3f',
];

def vec2i(x = 0, y = 0):
    return np.array([x, y], dtype = np.int32);

def vec2f(x  = 0., y = 0.):
    return np.array([x, y], dtype = np.float32);

def vec3i(x = 0, y = 0, z = 0):
    return np.array([x, y, z], dtype = np.int32);

def vec3f(x = 0, y = 0., z = 0.):
    return np.array([x, y, z], dtype = np.float32);
