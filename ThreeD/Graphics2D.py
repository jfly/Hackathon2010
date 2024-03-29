import curses
import ThreeD.Polygon3D as p3d

pixel = ' '

# TODO: Make an orange color using init_color
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)
curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)
curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)
curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_RED)
curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_YELLOW)
white   = curses.color_pair(1)
black   = curses.color_pair(2)
blue    = curses.color_pair(3)
cyan    = curses.color_pair(4)
green   = curses.color_pair(5)
magenta = curses.color_pair(6)
red     = curses.color_pair(7)
yellow  = curses.color_pair(8)
color_map = {curses.COLOR_WHITE : white, curses.COLOR_BLACK : black,
             curses.COLOR_BLUE : blue, curses.COLOR_CYAN : cyan,
             curses.COLOR_GREEN : green, curses.COLOR_MAGENTA : magenta,
             curses.COLOR_RED : red, curses.COLOR_YELLOW : yellow}

# If you're using this library, we assume that you've called curses.start_color() first
def draw_line(screen, start, end, color=curses.COLOR_WHITE):
    __edge__(screen, start, end, color)


def __edge__(screen, start, end, color):
    color = color_map[color]
    
    if type(screen) != list:
        start = legalize(screen, start)
        end = legalize(screen, end)
    
        screen.addch(int(start[1]), int(start[0]), pixel, color)
        
    if start == end: #we're just drawing a point
        return

    if (abs(start[0] - end[0]) > abs(start[1] - end[1])):
        slope = (start[1] - end[1]) / (1.0 * start[0] - end[0])
        if start[0] > end[0]:
            start, end = end, start
        y = start[1]
        for x in range(int(start[0]), int(end[0])):
            if type(screen) == list:
                screen.append((int(round(x)), int(y)))
            else:
                screen.addch(int(round(y)), int(x), pixel, color)
            y += slope
    else:
        slope = (1.0 * start[0] - end[0]) / (start[1] - end[1])
        if start[1] > end[1]:
            start, end = end, start
        x = start[0]
        for y in range(int(start[1]), int(end[1])):
            if type(screen) == list:
                screen.append((int(x), int(round(y))))
            else:
                screen.addch(int(y), int(round(x)), pixel, color)
            x += slope
    if type(screen) != list:
        screen.addch(int(end[1]), int(end[0]), pixel, color)
    

# For now, assuming that POLY is a (2D convex) quadrilateral
def fill_polygon(screen, poly, color=curses.COLOR_WHITE):
    boundary = []
    for el in poly:
        boundary.append(el)
    for i in range(len(poly)):
        __edge__(boundary, poly[i], poly[(i+1)%len(poly)], color)
    boundary = split_by_x(boundary)
    for x, L in boundary.items():
        low  = min(L)
        high = max(L)
        draw_line(screen, (x,low), (x,high), color)

# TODO: Something's not quite right, but I don't know what
def stroke_polygon(screen, poly, color=curses.COLOR_WHITE):
    boundary = []
    for el in poly:
        boundary.append(el)
    for i in range(len(poly)):
        __edge__(boundary, poly[i], poly[(i+1)%len(poly)], color)
    boundary = split_by_x(boundary)
    color = color_map[color]
    for x, L in boundary.items():
        for y in L:
            (x,y) = legalize(screen, (x,y))
            screen.addch(int(y), int(x), pixel, color)
    #for i in range(len(poly)):
    #    __edge__(screen, poly[i], poly[(i+1)%len(poly)], color)

def draw_polygon(screen, poly, fill=curses.COLOR_WHITE, stroke=curses.COLOR_WHITE):
    if fill != None:
        fill_polygon(screen, poly, fill)
    if stroke != None:
        stroke_polygon(screen, poly, stroke)

def split_by_x(points):
    result = {}
    for x,y in points:
        if x in result:
            result[x].append(y)
        else:
            result[x] = [y]
    return result

def legalize(screen, point):
    height, width = screen.getmaxyx()
    x = max(min(width-2, point[0]), 0) # TODO: Weird edge case find actual width
    y = max(min(height-2, point[1]), 0) # of terminal
    return x,y
