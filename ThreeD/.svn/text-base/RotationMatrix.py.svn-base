import math

SIZE = 3
class RotationMatrix:
    def __init__(self, new_data=None):
        if new_data == None:
            self.data = [ [ 0 for j in range(0, SIZE) ] for i in range(0, SIZE) ]
            # fill in 1s of an identity matrix
            for i in range(0, SIZE):
                self.data[i][i] = 1
        else:
            if type(new_data) == list or type(new_data) == tuple:
                if type(new_data[0]) == list or type(new_data[0]) == tuple:
                    self.data = new_data
                else:
                    # converting a point to a matrix
                    self.data = [ [ new_data[i] ] for i in range(0, SIZE) ]
            
    def setRotation(self, ax, degrees_CCW):
        self.axis = ax
        self.degreesCCW = degrees_CCW
        self.data = [ [ 0 for j in range(0, SIZE) ] for i in range(0, SIZE) ]
        rows = [0, 1, 2]
        rows.remove(self.axis)
        if self.axis == 1:
            sin = -1
        else:
            sin = 1
        sin *= math.sin(math.radians(self.degreesCCW))
        cos = math.cos(math.radians(self.degreesCCW))
        for c in range(0, SIZE):
            if c == self.axis:
                self.data[c][c] = 1
            else:
                self.data[rows[0]][c] = cos
                self.data[rows[1]][c] = sin
                s = sin
                sin = cos
                cos = -s
        return self
    
    def rotationMatrix(self, (lx, ly, lz), degreesCCW ):
        #normalize the vector to rotate about
        (lx2, ly2, lz2)  = (lx*lx, ly*ly, lz*lz)
        scale = math.sqrt( lx2 + ly2 + lz2 )
        (lx, ly, lz) = (lx/scale, ly/scale, lz/scale)
        (lx2, ly2, lz2)  = (lx*lx, ly*ly, lz*lz)
        c = math.cos( math.radians( degreesCCW ) )
        s = math.sin( math.radians( degreesCCW ) )
        self.data = [ [ lx2 + (1-lx2)*c, lx*ly*(1-c) - lz*s, lx*lz*(1-c) + ly*s ], \
                     [ lx*ly*(1-c) + lz*s, ly2 + (1-ly2)*c, ly*lz*(1-c) - lx*s ], \
                     [ lx*lz*(1-c) - ly*s, ly*lz*(1-c) + lx*s, lz2 + (1-lz2)*c ] ]
        return self

    # TODO
    def invert(self):
        (a, b, c, d, e, f, g, h, i) = (self.data[0][0], self.data[0][1], self.data[0][2], \
                                       self.data[1][0], self.data[1][1], self.data[1][2], \
                                       self.data[2][0], self.data[2][1], self.data[2][2])
        det = a*(e*i-f*h) - b*(d*i-f*g) + c*(d*h-e*g)
        M = RotationMatrix([[(e*i-f*h)/det, (c*h-b*i)/det, (b*f-c*e)/det],\
             [(f*g-d*i)/det, (a*i-c*g)/det, (c*d-a*f)/det],\
             [(d*h-e*g)/det, (b*g-a*h)/det, (a*e-b*d)/det]])
        return M

    def multiply(self, m):
        matchingSide = len(self.data[0])
        if matchingSide != len(m.data):
            return None
        result = RotationMatrix([ [ 0 for j in range(0, len(m.data[0])) ] for i in range(0, len(self.data)) ])
        
        for i in range(0, len(result.data)):
            for j in range(0, len(result.data[0])):
                dot = 0
                for ch in range(0, matchingSide):
                    dot += self.data[i][ch] * m.data[ch][j]
                result.data[i][j] = dot
        return result
    
    def multiplyPoint(self, point):
        return self.multiply(RotationMatrix(point)).transpose().data[0]
        
    def transpose(self):
        t = RotationMatrix([ [ 0 for j in range(0, len(self.data)) ] for i in range(0, len(self.data[0])) ])
        for i in range(0, len(t.data)):
            for j in range(0, len(t.data[0])):
                t.data[i][j] = self.data[j][i];
        return t;

    def scaleRotation(self, scale):
        return RotationMatrix(self.axis, scale*self.degreesCCW);

    def isIdentity(self, tolerance = 0):
        return self.equals(RotationMatrix(), tolerance);
    
    def __eq__(self, other):
        return not other == None and self.equals(other, 0);

    def equals(self, other, tolerance):
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data[i])):
                if abs(self.data[i][j] - other.data[i][j]) > tolerance:
                    return False;
        return True;
    
    def __str__(self):
#        return str(self.data)
        s = ""
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data[0])):
                s += "  %s" % str(self.data[i][j])
            s += "\n"
        return "[" + s[1:len(s)-1] + " ]\n"

def main():
#    print(RotationMatrix().setRotation(1, 30.))
#    print(RotationMatrix().setRotation(1, 30./5))
#    print(RotationMatrix().setRotation(1, 30.).multiply(RotationMatrix().setRotation(0, 180.)))
    print(RotationMatrix().setRotation(1, 30./5)).multiplyPoint([1, 2, 3])
#    print RotationMatrix([1, 2, 3])
#    print RotationMatrix([1, 2, 3]).transpose()

if __name__ == "__main__":
    main()
