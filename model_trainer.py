class Model_Trainer:
    def __init__(self, dataset_path, model_output_path, k_folds):
        self.__dataset_path = dataset_path
        self.__model_output_path = model_output_path
        self.__k_folds = k_folds

    def load_dataset(self):
        pass

    def train(self,X_train, y_train):
        pass

    def evaluate(self, model, X_val, y_val):
        pass

    def cross_validate(self, X, y):
        pass

    def retrain_full(self, X, y):
        pass

    def save_model(self, model):
        pass

    def run(self):
        pass