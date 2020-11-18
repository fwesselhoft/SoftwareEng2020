import tkinter as tk
from PIL import ImageTk, Image
import time

BOARDW = 600
BOARDH = 600
BOARDWS = BOARDW/7
BOARDHS = BOARDH/7


class GameBoard():

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('ClueLess')
        self.canvas = tk.Canvas(self.window, width = BOARDH, height = BOARDW)
        self.canvas.pack()
        self.image = None
        self.initialize_board()

    def mainloop(self):
        self.window.mainloop()


    def initialize_board(self):
        for i in range(6):
            self.canvas.create_line(i*BOARDHS+1, 1, i*BOARDWS+1, 5*BOARDHS+1)

        for i in range(6):
            self.canvas.create_line(1, i*BOARDHS+1, 5*BOARDWS+1, i*BOARDWS+1)

    def set_position(self, Player):
        return self.canvas.create_image((Player.x +.25) * BOARDWS, (Player.y+.15)*BOARDHS, anchor='nw', image=Player.img)

    def move_piece(self, piece, dx, dy):
        for _ in range(int(BOARDWS)):
            self.canvas.move(piece, dx, dy)
            self.window.update()
            time.sleep(.02)



class Player():


    def __init__(self, GB, info):
        self.GB = GB
        self.name = info['name']
        self.img = ImageTk.PhotoImage(Image.open(f"static/{info['img_path']}"))
        self.x = info['start_x']
        self.y = info['start_y']
        self.piece = self.GB.set_position(self) 

    def move_piece(self, x, y):
        print('here')
        dx = x-self.x
        dy = y-self.y
        print(dx, dy)
        self.GB.move_piece(self.piece, dx, dy)
        self.x = x
        self.y = y





GB = GameBoard()
MSC = Player(GB, {'name':'Scar', 'img_path':'scarlet.jpg', 'start_x':0, 'start_y':0})
MSC.move_piece(0,1)
time.sleep(2)
MSC.move_piece(0,0)
time.sleep(2)
MSC.move_piece(4,4)

GB.mainloop()

