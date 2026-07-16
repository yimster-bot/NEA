class User:
    def __init__(self, userID, name, email):
        self.__userID = userID
        self.__name = name
        self.__email = email
        self.__password_hash = ''
        self.__is_logged_in = False

    def get_name(self):
        return self.__name

    def get_userID(self):
        return self.__userID

    def get_is_logged_in(self):
        return self.__is_logged_in

    def create_account(self, email, password):
        pass

    def login(self, email, password):
        pass

    def verify_password(self, input_password):
        pass

    def logout(self):
        pass
