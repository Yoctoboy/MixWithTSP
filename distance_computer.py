class DistanceComputer(object):

    def __init__(self, start_node, end_node):
        """
        Constructor for the DistanceComputer
        
        Arguments:
            start_node {dict} -- start_node of the distance to compute
            end_node {dict} -- end node of th distance to computer
        """

        self.start_node = start_node
        self.end_node = end_node

    def compute(self):
        result = 0
        result += self._get_shift_distance()
        result += self._get_bpm_distance()
        result += self._get_bonus_shifted_distance()
        return int(result ** 1.3)
    
    def _are_shifts_compatible(self):

        start_tone, end_tone = self.start_node["key_tone"], self.end_node["key_tone"]
        return (
            (start_tone == end_tone) or
            (start_tone[1] != end_tone[1] and start_tone[0] == end_tone[0]) or
            (start_tone[1] == end_tone[1] and (abs(start_tone[0] - end_tone[0]) % 12) <= 1)
        )
    
    def _get_shift_distance(self):
        return 500 * (1 - self._are_shifts_compatible())

    def _get_bpm_distance(self):
        start_bpm, end_bpm = self.start_node["bpm"], self.end_node["bpm"]
        # relative_period_diff = start_period / end_period (what to do with this ?)
        return int((abs(start_bpm - end_bpm) / end_bpm) * 250) ** 2

    def _get_bonus_shifted_distance(self):
        return 75 * (self.start_node["shift"] ** 2) + 75 * (self.end_node["shift"] ** 2)
        