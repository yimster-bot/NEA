from pitch import Pitch
from xg_model import xG_Model
from feature_calculation import Feature_Calculation


class Application:
    def __init__(self):
        self.__root = None
        self.__current_user = None
        self.__pitch = Pitch()
        self.__simulation = None
        self.__model = xG_Model('model.pkl')
        self.__calculator = Feature_Calculation('scaler.pkl')
        self.__renderer = None
        self.__manager = None
        self.__display = None

    def start(self):
        pass

    def login_screen(self):
        pass

    def create_account_screen(self):
        pass

    def home_screen(self):
        pass

    def new_simulation_screen(self):
        pass

    def results_screen(self):
        pass

    def comparison_screen(self):
        pass

    def split_results_screen(self):
        pass

    def general_loading_screen(self):
        pass

    def special_loading_screen(self):
        pass

    def settings_screen(self):
        pass