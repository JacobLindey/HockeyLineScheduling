from Team import Team
import copy


class Path:

    def __init__(self):
        self.team = Team()
        self.lines_sequence = []
        self.value = 0

    def __str__(self):
        string = "Value: {v:4.2f} \n".format(v=self.value)
        for line in self.lines_sequence:
            string += str(line) + '\n'
        return string

    def __getitem__(self, item):
        return self.lines_sequence[item]

    def add(self, line):
        self.lines_sequence.append(line)

    def copy(self):
        temp_path = Path()
        temp_path.team = self.team.copy()
        temp_path.lines_sequence = copy.deepcopy(self.lines_sequence)
        temp_path.value = copy.copy(self.value)
        return temp_path

    def evaluate(self):
        cumulative_value = 0
        for frame in self.lines_sequence:
            cumulative_value += frame.goal_differential * frame.fatigue_level
        self.value = cumulative_value
