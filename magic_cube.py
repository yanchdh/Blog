# -*- co'D'ing:'U't'F'-8 -*-
import numpy as np
import random

# up, down, left, right, front, behind
U, D, L, R, F, B = 0, 1, 2, 3, 4, 5
VIEW = [U, D, L, R, F, B]
COLOR = ['U', 'D', 'L', 'R', 'F', 'B']

class MagicCube(object):
    @staticmethod
    def generatorMagicCube(n):
        cube_data = []
        for view in VIEW:
            cube_data.append([[COLOR[view]] * n for i in range(n)])
        return np.array(cube_data)
    
    @staticmethod
    def show(cube_data, view):
        print COLOR[view]
        print cube_data[view]
    
    #FLU rotate algorithm
    @staticmethod
    def rotate(cube_data, view, clockwise):
        view_data = cube_data[view]
        view_data[:] = zip(*view_data[::-1]) if clockwise else zip(*view_data)[::-1]
        a, b, c, d = None, None, None, None
        if view == U or view == D:
            _f = _l = _b = _r = 0 if view == U else -1
            a, b, c, d = cube_data[F, _f, :], cube_data[R, _r, :], cube_data[B, _b, :], cube_data[L, _l, :]
        elif view == F or view == B:
            _u = _d = 0 if view == B else -1
            _r = 0 if view == F else -1
            _l = 0 if view == B else -1
            a, b, c, d = cube_data[U, _u, :], cube_data[L, :, _l], cube_data[D, _d, :], cube_data[R, :, _r]
        elif view == L or view == R:
            _u = _d = 0 if view == L else -1
            _f = 0 if view == L else -1
            _b = 0 if view == R else -1
            a, b, c, d = cube_data[U, :, _u], cube_data[F, :, _f], cube_data[D, :, _d], cube_data[B, :, _b]
        if not clockwise:
            a, b, c, d = a, d, c, b
        a[:], b[:], c[:], d[:] = b, c, d, a.copy()
    
    @staticmethod
    def disrupt(cube_data, times):
        for i in range(times):
            view = random.randint(0, len(VIEW) - 1)
            clockwise = random.randint(0, 1)
            MagicCube.rotate(cube_data, view, clockwise)
    
    # score, 2 or more generation deep search 
    @staticmethod
    def solveMagicCube(n, init_state, target_state):
        state_set = set()
        que1, que2 = [], []
        state_set.add(init_state)
        que1.append(init_state)
        min_num = map(cmp, init_state, target_state).count(0)
        step = 0
        while que1:
            step += 1
            while que1:
                cur_state = que1.pop()
                cur_cube_data = np.array(list(cur_state)).reshape((6, n, n))
                for clockwise in [True, False]:
                    for view in VIEW:
                        MagicCube.rotate(cur_cube_data, view, clockwise)
                        new_state = cur_cube_data.tostring()
                        MagicCube.rotate(cur_cube_data, view, not clockwise)
                        if new_state in state_set:
                            continue
                        if new_state == target_state:
                            print 'find it', step
                            return
                        new_num = map(cmp, new_state, target_state).count(0)
                        if new_num < min_num:
                            continue
                        state_set.add(new_state)
                        que2.append(new_state)
            que1, que2 = que2, que1
            min_num += 1
            print 'step', step, 'state_num', len(que1), 'min_num', min_num
        print 'not find'

n = 3
times = 7
cube_data = MagicCube.generatorMagicCube(n)
target_state = cube_data.tostring()
MagicCube.disrupt(cube_data, times)
init_state = cube_data.tostring()

print 'init_state', init_state
print 'target_state', target_state
MagicCube.solveMagicCube(n, init_state, target_state)