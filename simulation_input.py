class Simulation_Input:
    def __init__(self, event_type, delivery_type, defender_shape, st_pos, deliverer_pos, gk_pos, attacker_pos):
        self.__event_type = event_type
        self.__delivery_type = delivery_type
        self.__defender_shape = defender_shape
        self.__st_pos = st_pos
        self.__deliverer_pos = deliverer_pos
        self.__gk_pos = gk_pos
        self.__attacker_pos = attacker_pos
        self.__is_direct = False
        self.__body_parts = [0, 1, 2, 3]

    def get_event_type(self):
        return self.__event_type

    def get_delivery_type(self):
        return self.__delivery_type

    def get_defender_shape(self):
        return self.__defender_shape

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

    def get_is_direct(self):
        return self.__is_direct

    def set_body_parts(self, body_parts):
        self.__body_parts = body_parts

    def get_body_parts(self):
        return self.__body_parts

    def check_direct(self):
        self.__is_direct = False
        if self.__event_type == 'Free kick' and self.__st_pos is not None and self.__deliverer_pos is not None:
            gap_x = self.__st_pos.get_real_x() - self.__deliverer_pos.get_real_x()
            gap_y = self.__st_pos.get_real_y() - self.__deliverer_pos.get_real_y()

            if gap_x**2 + gap_y **2 <=1:
                self.__is_direct = True

        if self.__is_direct:
            self.__delivery_type = -1
            self.__body_parts = [1, 2]
        else:
            self.__body_parts = [0, 1, 2, 3]


    def validate(self, pitch_length, pitch_width):
        if self.__event_type == 'Select option' or self.__defender_shape == 'Select option':
            return 'Choose an event type and defender configuration'
        if not self.__is_direct and self.__delivery_type == 'Select option':
            return 'Choose a delivery type'
        if self.__st_pos is None:
            return 'Place a shooter on the pitch'
        if self.__deliverer_pos is None:
            return 'Place a deliverer on the pitch'
        if self.__gk_pos is None:
            return 'Place a goalkeeper on the pitch'

        for player in [self.__st_pos, self.__deliverer_pos, self.__gk_pos] + self.__attacker_pos:
            if not player.within_bounds(pitch_length, pitch_width):
                return f'{player.get_role()} is outside the attacking half'

        return None


    def to_dict(self):
        return {
            'event_type': self.__event_type,
            'delivery_type': self.__delivery_type,
            'defender_shape': self.__defender_shape,
            'is_direct': self.__is_direct,
            'body_parts': self.__body_parts,
            'shooter': self.__st_pos.to_dict(),
            'deliverer': self.__deliverer_pos.to_dict(),
            'goalkeeper': self.__gk_pos.to_dict(),
            'attackers': [attacker.to_dict() for attacker in self.__attacker_pos]
        }