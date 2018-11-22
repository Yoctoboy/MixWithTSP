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
        if self.start_node == 0:
            result = self._get_bonus_shifted_distance()
        elif self.end_node == 0:
            result = 0
        elif not (self._are_bpm_compatible() and self._are_tones_compatible()):
            result = 1000000
            result += self._get_bonus_shifted_distance()
        else:
            result = 0
            result += self._get_bpm_distance()
            result += self._get_bonus_shifted_distance()
            result = int(result ** 1.3)
        return result
    
    def _are_tones_compatible(self):

        start_tone, end_tone = self.start_node["shifted_key_tone"], self.end_node["shifted_key_tone"]
        return (
            (start_tone == end_tone) or
            (start_tone[1] != end_tone[1] and start_tone[0] == end_tone[0]) or
            (start_tone[1] == end_tone[1] and (abs(start_tone[0] - end_tone[0]) % 12) <= 1)
        )
    
    def _are_bpm_compatible(self):
        start_bpm, end_bpm = float(self.start_node["bpm"]), float(self.end_node["bpm"])
        return (abs(start_bpm - end_bpm) / end_bpm) < 0.06

    def _get_bpm_distance(self):
        start_bpm, end_bpm = self.start_node["bpm"], self.end_node["bpm"]
        # relative_period_diff = start_period / end_period (what to do with this ?)
        return int((abs(start_bpm - end_bpm) / end_bpm) * 250) ** 2

    def _get_bonus_shifted_distance(self):
        return 225 * (self.end_node["shift"] ** 2)
