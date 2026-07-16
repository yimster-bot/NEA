class xG_Model:
    def __init__(self, model_path):
        self.__model_path = model_path
        self.__model = None
        self.__is_loaded = False

    def get_is_loaded(self):
        return self.__is_loaded

    def load_model(self):
        pass

    def predict(self, feature_vectors):
        pass