class Defender_Render:
    zonal_positions = [(-9, 5.5), (-3, 5.5), (3, 5.5), (9, 5.5),
                         (-6, 11), (0, 11), (6, 11), (-2, 2)]
    mixed_zones = [(-6, 5.5), (0, 5.5), (6, 5.5)]
    max_defenders = 10

    def __init__(self, pitch, defender_shape):
        self.__pitch = pitch
        self.__defender_shape = defender_shape

    def render(self, attacker_positions):
        self.__pitch.clear_role('Defender')
        if self.__defender_shape == 'Zonal':
            self.render_zonal()
        if self.__defender_shape == 'Man marking':
            self.render_man_marking(attacker_positions)
        if self.__defender_shape == 'Mixed':
            self.render_mixed(attacker_positions)
        if self.__defender_shape == 'No defense':
            self.__pitch.clear_role('Defender')

    def place_in_zone(self, offset, depth):
        across = self.__pitch.get_pitch_width() / 2 + offset
        pixel_x, pixel_y = self.__pitch.to_pixels(across, depth)
        self.__pitch.draw_players(pixel_x, pixel_y, 'Defender')
        return pixel_x, pixel_y

    def mark(self, attacker_x, attacker_y):
        goal_side = 1.5*self.__pitch.get_scale()
        defender_y = max(attacker_y - goal_side, self.__pitch.get_margin())
        self.__pitch.draw_players(attacker_x, defender_y, 'Defender')

    def render_zonal(self):
        for offset, depth in self.zonal_positions:
            self.place_in_zone(offset, depth)

    def render_mixed(self, attacker_positions):
        zone_defenders = [self.place_in_zone(offset, depth) for offset, depth in self.mixed_zones]
        cover_distance = 3*self.__pitch.get_scale()
        markers_left = self.max_defenders - len(zone_defenders)
        for attacker_x, attacker_y in attacker_positions:
            if markers_left == 0:
                break
            covered = False
            for zone_x, zone_y in zone_defenders:
                if (attacker_x - zone_x)**2 + (attacker_y - zone_y)**2 <= cover_distance**2:
                    covered = True
            if not covered:
                self.mark(attacker_x, attacker_y)
                markers_left -=1

    def render_man_marking(self, attacker_positions):
        for attacker_x, attacker_y in attacker_positions[:self.max_defenders]:
            self.mark(attacker_x, attacker_y)
