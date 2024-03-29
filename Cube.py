import curses
import ThreeD.Polygon3D as p3d
from ThreeD.RotationMatrix import RotationMatrix
from copy import copy

CUBE_SIDE_LEN = 15
HALF_SIDE_LEN = CUBE_SIDE_LEN / 2.
CUBIE_SIDE_LEN = CUBE_SIDE_LEN / 3.
FRAMES_ANIMATION = 3
COLOR_SCHEME = { "U": curses.COLOR_WHITE,
                 "D": curses.COLOR_YELLOW,
                 "R": curses.COLOR_RED,
                 "L": curses.COLOR_MAGENTA,
                 "F": curses.COLOR_GREEN,
                 "B": curses.COLOR_BLUE }
BORDER_COLOR = curses.COLOR_BLACK

KEYS = {"e":"L'",
"d":"L",
"r":"l'",
"v":"l",
"E":"l'",
"D":"l",

"f":"U'",
"j":"U",
"F":"u'",
"J":"u",

"k":"R'",
"i":"R",
"m":"r'",
"u":"r",
"K":"r'",
"I":"r",

"g":"F'",
"h":"F",
"G":"f'",
"H":"f",

"l":"D'",
"s":"D",
"L":"d'",
"S":"d",

"w":"B",
"o":"B'",
"W":"b",
"O":"b'",

"q":"z'",
"p":"z",

"a":"y'",
";":"y",

"t":"x",
"y":"x",
"b":"x'",
"n": "x'",

" ": "scramble"
}

class Cube:
    def __init__(self):
        self.faces = {}
        self.all_polys = []
        self.x_axis = [ 1, 0, 0 ]
        self.y_axis = [ 0, 1, 0 ]
        self.z_axis = [ 0, 0, 1 ]
        self.net_rotation = RotationMatrix()
        self.history = []
        self.history_index = 0

        up = []

        for j in range(3):
            for i in range(3):
                u = p3d.Polygon3D(COLOR_SCHEME['U'], BORDER_COLOR)
                p1 = (-HALF_SIDE_LEN + i * CUBIE_SIDE_LEN, HALF_SIDE_LEN, -HALF_SIDE_LEN + j * CUBIE_SIDE_LEN)
                p2 = (-HALF_SIDE_LEN + (i + 1) * CUBIE_SIDE_LEN, HALF_SIDE_LEN, -HALF_SIDE_LEN + j * CUBIE_SIDE_LEN)
                p3 = (-HALF_SIDE_LEN + (i + 1) * CUBIE_SIDE_LEN, HALF_SIDE_LEN, -HALF_SIDE_LEN + (j + 1) * CUBIE_SIDE_LEN)
                p4 = (-HALF_SIDE_LEN + i * CUBIE_SIDE_LEN, HALF_SIDE_LEN, -HALF_SIDE_LEN + (j + 1) * CUBIE_SIDE_LEN)
                u.add_points([p1, p2, p3, p4])
                up.append(copy(u))
        
        front = []
        for poly in up:
            front.append(copy(poly))
        f_rot = RotationMatrix().setRotation(0, 90)
        for i in range(len(front)):
            front[i].rotate(f_rot)
            front[i].fill = COLOR_SCHEME['F']

        back = []
        for poly in up:
            back.append(copy(poly))
        b_rot1 = RotationMatrix().setRotation(1, 180)
        b_rot2 = RotationMatrix().setRotation(0, -90)
        for i in range(len(back)):
            back[i].rotate(b_rot1)
            back[i].rotate(b_rot2)
            back[i].fill = COLOR_SCHEME['B']

        left = []
        for poly in up:
            left.append(copy(poly))
        l_rot1 = RotationMatrix().setRotation(0, 90)
        l_rot2 = RotationMatrix().setRotation(1, -90)
        for i in range(len(left)):
            left[i].rotate(l_rot1)
            left[i].rotate(l_rot2)
            left[i].fill = COLOR_SCHEME['L']

        right = []
        for poly in up:
            right.append(copy(poly))
        r_rot1 = RotationMatrix().setRotation(0, 90)
        r_rot2 = RotationMatrix().setRotation(1, 90)
        for i in range(len(right)):
            right[i].rotate(r_rot1)
            right[i].rotate(r_rot2)
            right[i].fill = COLOR_SCHEME['R']

        down = []
        for poly in up:
            down.append(copy(poly))
        d_rot = RotationMatrix().setRotation(0, 180)
        for i in range(len(down)):
            down[i].rotate(d_rot)
            down[i].fill = COLOR_SCHEME['D']
        
        self.faces['B'] = back
        self.faces['F'] = front
        self.faces['U'] = up
        self.faces['D'] = down
        self.faces['L'] = left
        self.faces['R'] = right
        
        for face in self.faces.values():
            self.all_polys += face
            
    def get_axis(self, face):
        face = face.upper()
        neg = lambda (x, y, z): (-x, -y, -z)
        if face == "U" or face == 'Y':
            return self.y_axis
        elif face == "D":
            return neg(self.y_axis)
        elif face == "F" or face == 'Z':
            return self.z_axis
        elif face == "B":
            return neg(self.z_axis)
        elif face == "L":
            return neg(self.x_axis)
        elif face == "R" or face == 'X':
            return self.x_axis
        else:
            return None
        
    def tick(self):
        if self.history_index < len(self.history):
            if self.animate_turn(self.history[self.history_index]):
                self.history_index += 1
                
    def char_pressed(self, ch):
        self.do_turn(KEYS.get(ch, None))
            
    def do_turn(self, turns):
        if turns == None: return
        for turn in turns.split():
            if turn == 'scramble':
                import scrambler
                self.do_turn(scrambler.gen_scramble_str(25))
            elif turn == 'reset':
                #TODO
                pass
            elif turn == 'undo':
                if len(self.history) == 0:
                    continue
                last = self.history[-1].copy()
                last['dir'] *= -1
                del last['total_degrees'] # otherwise, we'll think the move is over
                self.history.append(last)
            else:
                face = turn[:1]
                dir = {"": 1, "'": -1, "2": 2, "2'": -2}[turn[1:]]
                if dir == None:
                    continue
                # can't store this axis now because it may change by the time we start animating
                if self.get_axis(face) == None:
                    continue
                if face in 'xyz':
                    face = {'x':'R', 'y':'U', 'z':'F'}[face]
                    layers = -1
                elif face.islower():
                    layers = 2
                else:
                    layers = 1
                
                self.history.append({'face': face, 'layers': layers, 'dir': dir})
                
    # cycles stickers in self.faces according to cycle
    def cycle_stickers(self, cycle):
        index = cycle[-1]
        last_poly = self.faces[index[0]][index[1]]
        for i in range(len(cycle)-1, 0, -1):
            index = cycle[i]
            index_prev = cycle[i-1]
            self.faces[index[0]][index[1]] = self.faces[index_prev[0]][index_prev[1]]
        index = cycle[0]
        self.faces[index[0]][index[1]] = last_poly

    def animate_turn(self, turn):
        total_degrees_ccw = -90*turn['dir']
        total_degrees = abs(total_degrees_ccw)
        inc_degree = 1.0*total_degrees_ccw / FRAMES_ANIMATION
        rot = RotationMatrix().rotationMatrix(self.get_axis(turn['face']), inc_degree)
        
        permutations = self.get_turn_permutations(turn)
        if permutations == None:
            return True
        for cycle in permutations:
            for index in cycle:
                self.faces[index[0]][index[1]].rotate(rot)
#        for poly in self.faces[turn['face']]:
#            poly.rotate(rot)
            
        turn['total_degrees'] = turn.get('total_degrees', 0) + abs(inc_degree)
        done = (turn['total_degrees'] >= total_degrees)
        if done:
            # updating internal representation
            for i in range(0, turn['dir'] % 4):
                for cycle in permutations:
                    self.cycle_stickers(cycle)
        return done 
        
    def get_turn_permutations(self, turn):
        (face, layers, dir) = (turn['face'], turn['layers'], turn['dir'])
        cycles = None
        if layers == -1:
            layers = 3
        if face == 'U':
            if layers == 1:
                cycles = [ [('U',0),('U',2),('U',8),('U',6)], [('U',1),('U',5),('U',7),('U',3)], [('F',0),('L',0),('B',0),('R',0)], [('F',1),('L',1),('B',1),('R',1)], [('F',2),('L',2),('B',2),('R',2)], [('U',4)] ]
            elif layers == 2:
                cycles = [ [('U',0),('U',2),('U',8),('U',6)], [('U',1),('U',5),('U',7),('U',3)], [('F',0),('L',0),('B',0),('R',0)], [('F',1),('L',1),('B',1),('R',1)], [('F',2),('L',2),('B',2),('R',2)], [('B',4),('R',4),('F',4),('L',4)], [('B',5),('R',5),('F',5),('L',5)], [('B',3),('R',3),('F',3),('L',3)], [('U',4)] ]
            elif layers == 3:
                cycles = [ [('U',0),('U',2),('U',8),('U',6)], [('U',1),('U',5),('U',7),('U',3)], [('F',0),('L',0),('B',0),('R',0)], [('F',1),('L',1),('B',1),('R',1)], [('F',2),('L',2),('B',2),('R',2)], [('B',4),('R',4),('F',4),('L',4)], [('B',5),('R',5),('F',5),('L',5)], [('B',3),('R',3),('F',3),('L',3)], [('U',4)], [('D',6),('D',8),('D',2),('D',0)], [('D',3),('D',7),('D',5),('D',1)], [('L',6),('B',6),('R',6),('F',6)], [('L',7),('B',7),('R',7),('F',7)], [('L',8),('B',8),('R',8),('F',8)], [('D',4)] ]
        elif face == 'F':
            if layers == 1:
                cycles = [ [('F',0),('F',2),('F',8),('F',6)], [('F',1),('F',5),('F',7),('F',3)], [('U',6),('R',0),('D',2),('L',8)], [('U',7),('R',3),('D',1),('L',5)], [('U',8),('R',6),('D',0),('L',2)], [('F',4)] ]  
            elif layers == 2:
                cycles = [ [('F',0),('F',2),('F',8),('F',6)], [('F',1),('F',5),('F',7),('F',3)], [('U',6),('R',0),('D',2),('L',8)], [('U',7),('R',3),('D',1),('L',5)], [('U',8),('R',6),('D',0),('L',2)], [('U',4),('R',4),('D',4),('L',4)], [('U',3),('R',1),('D',5),('L',7)], [('U',5),('R',7),('D',3),('L',1)], [('F',4)] ]  
            elif layers == 3:
                cycles = [ [('F',0),('F',2),('F',8),('F',6)], [('F',1),('F',5),('F',7),('F',3)], [('U',6),('R',0),('D',2),('L',8)], [('U',7),('R',3),('D',1),('L',5)], [('U',8),('R',6),('D',0),('L',2)], [('U',4),('R',4),('D',4),('L',4)], [('U',3),('R',1),('D',5),('L',7)], [('U',5),('R',7),('D',3),('L',1)], [('F',4)], [('B',6),('B',8),('B',2),('B',0)], [('B',3),('B',7),('B',5),('B',1)], [('R',8),('D',6),('L',0),('U',2)], [('R',5),('D',7),('L',3),('U',1)], [('R',2),('D',8),('L',6),('U',0)], [('B',4)] ]  
        elif face == 'R':
            if layers == 1:
                cycles = [ [('R',0),('R',2),('R',8),('R',6)], [('R',1),('R',5),('R',7),('R',3)], [('U',8),('B',0),('D',8),('F',8)], [('U',5),('B',3),('D',5),('F',5)], [('U',2),('B',6),('D',2),('F',2)], [('R',4)] ]
            elif layers == 2:
                cycles = [ [('R',0),('R',2),('R',8),('R',6)], [('R',1),('R',5),('R',7),('R',3)], [('U',8),('B',0),('D',8),('F',8)], [('U',5),('B',3),('D',5),('F',5)], [('U',2),('B',6),('D',2),('F',2)], [('U',4),('B',4),('D',4),('F',4)], [('U',7),('B',1),('D',7),('F',7)], [('U',1),('B',7),('D',1),('F',1)], [('R',4)] ]
            elif layers == 3:
                cycles = [ [('R',0),('R',2),('R',8),('R',6)], [('R',1),('R',5),('R',7),('R',3)], [('U',8),('B',0),('D',8),('F',8)], [('U',5),('B',3),('D',5),('F',5)], [('U',2),('B',6),('D',2),('F',2)], [('U',4),('B',4),('D',4),('F',4)], [('U',7),('B',1),('D',7),('F',7)], [('U',1),('B',7),('D',1),('F',1)], [('R',4)], [('L',6),('L',8),('L',2),('L',0)], [('L',3),('L',7),('L',5),('L',1)], [('B',8),('D',0),('F',0),('U',0)], [('B',5),('D',3),('F',3),('U',3)], [('B',2),('D',6),('F',6),('U',6)], [('L',4)] ]
        elif face == 'B':
            if layers == 1:
                cycles = [ [('B',0),('B',2),('B',8),('B',6)], [('B',1),('B',5),('B',7),('B',3)], [('U',2),('L',0),('D',6),('R',8)], [('U',1),('L',3),('D',7),('R',5)], [('U',0),('L',6),('D',8),('R',2)], [('B',4)] ]
            elif layers == 2:
                cycles = [ [('B',0),('B',2),('B',8),('B',6)], [('B',1),('B',5),('B',7),('B',3)], [('U',2),('L',0),('D',6),('R',8)], [('U',1),('L',3),('D',7),('R',5)], [('U',0),('L',6),('D',8),('R',2)], [('U',4),('R',4),('D',4),('L',4)], [('U',5),('L',1),('D',3),('R',7)], [('U',3),('L',7),('D',5),('R',1)], [('B',4)] ]
            elif layers == 3:
                cycles = [ [('B',0),('B',2),('B',8),('B',6)], [('B',1),('B',5),('B',7),('B',3)], [('U',2),('L',0),('D',6),('R',8)], [('U',1),('L',3),('D',7),('R',5)], [('U',0),('L',6),('D',8),('R',2)], [('U',4),('R',4),('D',4),('L',4)], [('U',5),('L',1),('D',3),('R',7)], [('U',3),('L',7),('D',5),('R',1)], [('B',4)], [('F',6),('F',8),('F',2),('F',0)], [('F',3),('F',7),('F',5),('F',1)], [('L',8),('D',2),('R',0),('U',6)], [('L',5),('D',1),('R',3),('U',7)], [('L',2),('D',0),('R',6),('U',8)], [('F',4)] ]
        elif face == 'L':
            if layers == 1:
                cycles = [ [('L',0),('L',2),('L',8),('L',6)], [('L',1),('L',5),('L',7),('L',3)], [('U',0),('F',0),('D',0),('B',8)], [('U',3),('F',3),('D',3),('B',5)], [('U',6),('F',6),('D',6),('B',2)], [('L',4)] ]
            elif layers == 2:
                cycles = [ [('L',0),('L',2),('L',8),('L',6)], [('L',1),('L',5),('L',7),('L',3)], [('U',0),('F',0),('D',0),('B',8)], [('U',3),('F',3),('D',3),('B',5)], [('U',6),('F',6),('D',6),('B',2)], [('U',4),('F',4),('D',4),('B',4)], [('U',1),('F',1),('D',1),('B',7)], [('U',7),('F',7),('D',7),('B',1)], [('L',4)] ]
            elif layers == 3:
                cycles = [ [('L',0),('L',2),('L',8),('L',6)], [('L',1),('L',5),('L',7),('L',3)], [('U',0),('F',0),('D',0),('B',8)], [('U',3),('F',3),('D',3),('B',5)], [('U',6),('F',6),('D',6),('B',2)], [('U',4),('F',4),('D',4),('B',4)], [('U',1),('F',1),('D',1),('B',7)], [('U',7),('F',7),('D',7),('B',1)], [('L',4)], [('R',6),('R',8),('R',2),('R',0)], [('R',3),('R',7),('R',5),('R',1)], [('F',8),('D',8),('B',0),('U',8)], [('F',5),('D',5),('B',3),('U',5)], [('F',2),('D',2),('B',6),('U',2)], [('R',4)] ]
        elif face == 'D':
            if layers == 1:
                cycles = [ [('D',0),('D',2),('D',8),('D',6)], [('D',1),('D',5),('D',7),('D',3)], [('F',6),('R',6),('B',6),('L',6)], [('F',7),('R',7),('B',7),('L',7)], [('F',8),('R',8),('B',8),('L',8)], [('D',4)] ]
            elif layers == 2:
                cycles = [ [('D',0),('D',2),('D',8),('D',6)], [('D',1),('D',5),('D',7),('D',3)], [('F',6),('R',6),('B',6),('L',6)], [('F',7),('R',7),('B',7),('L',7)], [('F',8),('R',8),('B',8),('L',8)], [('F',4),('R',4),('B',4),('L',4)], [('F',3),('R',3),('B',3),('L',3)], [('U',5),('R',5),('B',5),('L',5)], [('D',4)] ]
            elif layers == 3:
                cycles = [ [('D',0),('D',2),('D',8),('D',6)], [('D',1),('D',5),('D',7),('D',3)], [('F',6),('R',6),('B',6),('L',6)], [('F',7),('R',7),('B',7),('L',7)], [('F',8),('R',8),('B',8),('L',8)], [('F',4),('R',4),('B',4),('L',4)], [('F',3),('R',3),('B',3),('L',3)], [('U',5),('R',5),('B',5),('L',5)], [('D',4)], [('U',6),('U',8),('U',2),('U',0)], [('U',3),('U',7),('U',5),('U',1)], [('R',0),('B',0),('L',0),('F',0)], [('R',1),('B',1),('L',1),('F',1)], [('R',2),('B',2),('L',2),('F',2)], [('U',4)] ]
        return cycles

    def polygons(self):
        return self.all_polys
    
    def rotate(self, rotation):
        if rotation == None:
            rotation = self.net_rotation.invert()
            
        self.net_rotation = rotation.multiply(self.net_rotation)
        self.x_axis = rotation.multiplyPoint(self.x_axis)
        self.y_axis = rotation.multiplyPoint(self.y_axis)
        self.z_axis = rotation.multiplyPoint(self.z_axis)
        for poly in self.polygons():
            poly.rotate(rotation)

    def is_solved(self):
        for face in COLOR_SCHEME.keys():
            color = self.faces[face][0].fill
            for poly in self.faces[face]:
                if color != poly.fill:
                    return False
        return True
