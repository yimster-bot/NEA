class Player:
    def __init__(self, pixel_x, pixel_y, role):
        self.__pixel_x = pixel_x
        self.__pixel_y = pixel_y
        self.__real_x = None
        self.__real_y = None
        self.__role = role

    def get_pixel_x(self):
        return self.__pixel_x

    def get_pixel_y(self):
        return self.__pixel_y

    def get_real_x(self):
        return self.__real_x

    def get_real_y(self):
        return self.__real_y

    def get_role(self):
        return self.__role

    def set_real_x(self, x):
        self.__real_x = x

    def set_real_y(self, y):
        self.__real_y = y

    def convert_coordinates(self, canvas_width, canvas_height, pitch_length, pitch_width):
        scale = canvas_width / pitch_width
        margin = canvas_height - (pitch_length/2)*scale
        self.__real_x = pitch_length - (self.__pixel_x - margin)/scale
        self.__real_y = self.__pixel_x/scale

    def within_bounds(self, pitch_length, pitch_width):
        return pitch_length/2 <= self.__real_x <= pitch_length and 0<=self.__real_y <= pitch_width

    def to_dict(self):
        return {'role': self.__role, 'pixel_x': self.__pixel_x, 'pixel_y': self.__pixel_y,
                'real_x': self.__real_x, 'real_y': self.__real_y}