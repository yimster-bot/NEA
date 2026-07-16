class Manage_Simulation:
    def __init__(self, save_directory, db_connection, current_user):
        self.__save_directory = save_directory
        self.__db_connection = db_connection
        self.__current_user = current_user

    def save_simulation(self, simulation, xg_results, shot_details, name):
        pass

    def load_simulation(self, file_path):
        pass

    def list_simulations(self, sort_mode):
        pass

    def delete_simulation(self, SimulationID):
        pass

    def validate_filepath(self,file_path):
        pass
