import tkinter as tk

class Pitch:
    def __init__(self):
        self.__pitch_length = 105
        self.__pitch_width = 68
        self.__scale = 10
        self.__margin = 30
        self.__canvas_width = self.__pitch_width*self.__scale
        self.__canvas_height = int(self.__pitch_length/2*self.__scale)+self.__margin
        self.__canvas = None
        self.__role_colours = {'Attacker': 'red', 'Goalkeeper': 'grey', 'Shooter': 'yellow', 'Deliverer': 'blue', 'Defender': 'black'}

    def get_canvas_width(self):
        return self.__canvas_width

    def get_canvas_height(self):
        return self.__canvas_height

    def get_pitch_length(self):
        return self.__pitch_length

    def get_pitch_width(self):
        return self.__pitch_width

    def get_scale(self):
        return self.__scale

    def get_margin(self):
        return self.__margin

    def get_role_colour(self, role):
        return self.__role_colours[role]

    def create_canvas(self, parent):
        self.__canvas = tk.Canvas(parent, width=self.__canvas_width, height=self.__canvas_height,
                                  bg='green', highlightthickness=0)
        return self.__canvas

    def to_pixels(self, across, depth):
        return across*self.__scale, (self.__margin+depth)*self.__scale

    def draw_pitch(self):
        canvas = self.__canvas

        #center circle
        canvas.create_oval(248.5, 463.5, 431.5, 646.5, outline='white', width=3)

        # center dot
        canvas.create_oval(335, 550, 345, 560, fill='white', outline='white')

        # penalty box
        canvas.create_rectangle(340-201.6, 29, 340+201.6, 195, outline='white', width=3)

        # goal box
        canvas.create_rectangle(340 - 91.6, 29, 340 + 91.6, 85, outline='white', width=3)

        #penalty dot
        canvas.create_oval(335, 135, 345, 145, fill='white', outline='white')

        # penalty arc
        canvas.create_arc(248.5, 48.5, 431.5, 231.5, start=216.9, extent=106.2, style=tk.ARC, outline='white', width=3)

        # corners
        canvas.create_oval(-10, 20, 10, 40, outline='white', width=3)
        canvas.create_oval(670, 20, 690, 40, outline='white', width=3)

        # pitch (covers the area above the goal line, same colour as the app background)
        canvas.create_rectangle(0, 0, 690, 30, fill='#F9F9F9', outline='#F9F9F9')

        # goal line
        canvas.create_line(0, 30, 680, 30, fill='white', width=3)

        #goal
        canvas.create_rectangle(303.4, 10, 376.6, 30, outline='white', width=3)


    def draw_players(self, pixel_x, pixel_y, role):
        colour = self.__role_colours[role]
        return self.__canvas.create_oval(pixel_x-5, pixel_y-5, pixel_x+5, pixel_y+5,
                                         fill=colour, outline='white', width=2, tags=('player', role))

    def clear_player(self, pixel_x, pixel_y):
        for item in self.__canvas.find_withtag('player'):
            x1, y1, x2, y2 = self.__canvas.coords(item)
            if (x1+x2)/2 == pixel_x and (y1+y2)/2 == pixel_y:
                self.__canvas.delete(item)
                return

    def clear_player(self, pixel_x, pixel_y):
        self.__canvas.delete(role)

    def clear_canvas(self):
        self.__canvas.delete('player')