class Simulation_Input:
    def __init__(self, event_type, delivery_type, st_pos, deliverer_pos, gk_pos, attacker_pos):
        self.__event_type = event_type
        self.__delivery_type = delivery_type
        self.__st_pos = st_pos
        self.__deliverer_pos = deliverer_pos
        self.__gk_pos = gk_pos
        self.__attacker_pos = attacker_pos
        self.__body_parts = []

    def get_event_type(self):
        return self.__event_type

    def get_delivery_type(self):
        return self.__delivery_type

    def get_st_pos(self):
        return self.__st_pos

    def get_deliverer_pos(self):
        return self.__deliverer_pos

    def get_gk_pos(self):
        return self.__gk_pos

    def get_attacker_pos(self):
        return self.__attacker_pos

    def get_body_parts(self):
        return self.__body_parts

    def set_body_parts(self, body_parts):
        self.__body_parts = body_parts

    def check_direct(self):
        pass

    def get_body_parts(self):
        pass

    def validate(self):
        pass

    def to_dict(self):
        pass