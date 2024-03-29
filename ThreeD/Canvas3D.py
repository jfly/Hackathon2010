import curses
import Graphics2D as g2d

EYE_Z = 25
PROJ_Z = 20
#TODO - find way to computed
CELL_HEIGHT_TO_WIDTH = 1.8
class Canvas3D:
    def __init__(self):
        self.polygons = []
        self.offset_z = 0
        self.scale = 3

    def add_poly(self, poly):
        self.polygons.append(poly)

    def clear_polys(self):
        self.polygons = []

    def add_polys(self, polys):
        self.polygons += polys

    def scaleCoordinate(self, coord, z):
        return coord * (EYE_Z - PROJ_Z) / (EYE_Z - z + self.offset_z)

    def toPoint2d(self, point3d):
        x, y, z = point3d
        return ( self.scaleCoordinate(x, z), self.scaleCoordinate(y, z) )
    
    def toPointWin(self, point3d, width, height):
        x, y = self.toPoint2d(point3d)
        
        return ( round(self.scale*x*CELL_HEIGHT_TO_WIDTH + width/2.), round(-self.scale*y + height/2.) )

    def draw(self, screen):
        height, width = screen.getmaxyx()
        self.polygons.sort()
        for poly in self.polygons:
            poly2d = []
            for point in poly.get_points():
                poly2d.append(self.toPointWin(point, width, height))
            g2d.draw_polygon(screen, poly2d, poly.get_fill(), poly.get_stroke())
