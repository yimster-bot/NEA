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
        pass

    def within_bounds(self, pitch_length, pitch_width):
        pass
