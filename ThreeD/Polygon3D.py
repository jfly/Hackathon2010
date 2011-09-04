import curses

class Polygon3D:
    def __init__(self, fill_color = curses.COLOR_WHITE, stroke_color = curses.COLOR_WHITE):
        self.points = []
        self.fill = fill_color
        self.stroke = stroke_color

    def add_point(self, point):
        self.points.append(point)

    def add_points(self, pts):
        self.points += pts
        
    def get_stroke(self):
        return self.stroke
    
    def get_fill(self):
        return self.fill
        
    def rotate(self, rotation):
        for i in range(0, len(self.points)):
            self.points[i] = rotation.multiplyPoint(self.points[i])

    def get_points(self):
        return self.points
    
    def aveZ(self):
        return sum([ p[2] for p in self.points ])/len(self.points)
    
    def __copy__(self):
        new = Polygon3D(self.fill, self.stroke)
        new.points = self.points[:]
        return new
    
    def __cmp__(self, other):
        # TODO - this is a quick hack to make things work for a cube
        return self.aveZ() - other.aveZ()