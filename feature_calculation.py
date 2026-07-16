class Feature_Calculation:
    def __init__(self, scaler_path):
        self.__scaler_path = scaler_path
        self.__dist_min = None
        self.__dist_max = None
        self.__angle_min = None
        self.__angle_max = None
        self.__gk_min = None
        self.__gk_max = None

    def load_scaler(self):
        pass

    def calculate_distance(self, st_pos):
        pass

    def calculate_angle(self, st_pos):
        pass

    def calculate_gk_distance(self, st_pos, gk_pos):
        pass

    def normalise(self, value, min_val, max_val):
        pass

    def build_feature_vector(self, norm_distance, norm_gk_distance, norm_angle, delivery_type, defender_shape, event_type, body_part):
        pass