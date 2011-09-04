import curses
import threading
from Cube import Cube
from ThreeD import RotationMatrix
from collections import deque

class MyThread (threading.Thread):
    def __init__(self):
        self.turns = deque([])
        threading.Thread.__init__(self)
        
    def run(self):
        self.infile = open('turnstream', 'r')
        self.running = True
        while self.running:
            self.turns.append(self.infile.readline())
        

def main(screen):
    import ThreeD.Graphics2D as g2d # Fix later
    from ThreeD.Canvas3D import Canvas3D
    
    try:
        curses.curs_set(0)
    except:
        pass
    curses.start_color()
   
    bkgd = g2d.white 
    screen.bkgd(' ', bkgd)

    cube = Cube()
    cube.rotate(RotationMatrix.RotationMatrix().setRotation(1, -45))
    cube.rotate(RotationMatrix.RotationMatrix().setRotation(0, 37))
    canvas = Canvas3D()
    canvas.add_polys(cube.polygons())
    canvas.offset_z += 8
    canvas.scale += 7
    
    screen.refresh()
    screen.timeout(0)

    read_thread = MyThread()
    read_thread.start()
    
    while 1:        
        ch = screen.getch()
        MOVE_AWAY = '<'
        MOVE_CLOSER = '>'
        ZOOM_OUT = ','
        ZOOM_IN = '.'
        RESET_VIEW = '1'
	FLIP_COLORS = '2'
        QUIT = '`'
        if ch == ord(QUIT):
            break
        elif ch == curses.KEY_LEFT:
            cube.rotate(RotationMatrix.RotationMatrix().setRotation(1, -30./10))
        elif ch == curses.KEY_RIGHT:
            cube.rotate(RotationMatrix.RotationMatrix().setRotation(1, 30./10))
        elif ch == curses.KEY_UP:
            cube.rotate(RotationMatrix.RotationMatrix().setRotation(0, -30./10))
        elif ch == curses.KEY_DOWN:
            cube.rotate(RotationMatrix.RotationMatrix().setRotation(0, 30./10))
        elif ch == ord(RESET_VIEW):
            cube.rotate(None)
	    cube.rotate(RotationMatrix.RotationMatrix().setRotation(1, -45))
	    cube.rotate(RotationMatrix.RotationMatrix().setRotation(0, 37))
        elif ch == ord(MOVE_AWAY):
            canvas.offset_z += .5
        elif ch == ord(MOVE_CLOSER):
            canvas.offset_z -= .5
        elif ch == ord(ZOOM_IN):
            canvas.scale += .1
        elif ch == ord(ZOOM_OUT):
            canvas.scale -= .1
	elif ch == ord(FLIP_COLORS):
	     bkgd = g2d.black if bkgd == g2d.white else g2d.white
	     screen.bkgd(' ', bkgd)
        elif 0 < ch < 256:
            cube.char_pressed(chr(ch))
        
        screen.erase()
        cube.tick()
        canvas.draw(screen)
        screen.addstr(15, 15, "zoom in " + ZOOM_IN)
        screen.addstr(16, 15, "zoom out " + ZOOM_OUT)
        screen.addstr(17, 15, "move away " + MOVE_AWAY)
        screen.addstr(18, 15, "move closer " + MOVE_CLOSER)
        screen.addstr(19, 15, "reset view " + RESET_VIEW)
        screen.addstr(20, 15, "flip colors " + FLIP_COLORS)
        screen.addstr(21, 15, "quit " + QUIT)
        screen.addstr(23, 15, "is solved? " + str(cube.is_solved()))

        if len(read_thread.turns) != 0:
            cube.do_turn(read_thread.turns.popleft())
    
    read_thread.running = False

if __name__ == '__main__':
    try:
		curses.wrapper(main)
    except:
    	import traceback
	traceback.print_exc()
    # need to use something stronger to kill the thread, lol
    import os
    os._exit(0)
