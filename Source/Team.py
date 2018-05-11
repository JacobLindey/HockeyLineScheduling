import copy
from CONSTANTS import *


class Team:

    def __init__(self):
        self.id = ""
        self.lines = []
        self.curr_line_index = 0

    def __str__(self):
        string = self.id + "\n"
        for i, line in enumerate(self.lines):
            string += str(i+1) + ": " + str(line) + "\n"
        return string

    def __getitem__(self, item):
        return self.lines[item]

    def copy(self):
        temp_team = Team()
        temp_team.id = self.id
        for line in self.lines:
            temp_team.add_line(line.copy())
        temp_team.curr_line_index = self.curr_line_index
        return temp_team

    def set_team(self, identifier, lines=[], start_line_index=0):
        self.id = identifier
        self.lines = lines
        self.curr_line_index = start_line_index

        for line in self.lines:
            line.on_ice = False
            line.toi = 0
            line.tob = 0
        self.lines[self.curr_line_index].on_ice = True
        self.lines[self.curr_line_index].toi = MIN_TOI

    def add_line(self, line):
        self.lines.append(line)

    def update(self, node, interval):
        """
        performs line switching and controls fatigue calculations
        :param node: line that currently being put on the ice
        :param interval: the length of time that has passed since last execution
        :return: None
        """
        for line in self.lines:
            if node.line_num == line.line_num:
                # switch onto ice
                if not line.on_ice:
                    line.on_ice = True
                    line.toi = MIN_TOI
                    line.tob = 0
                    self.curr_line_index = line.line_num
                else:
                    line.toi -= interval
            else:
                if line.on_ice:
                    line.on_ice = False
                    line.tob = MIN_TOB
                    line.toi = 0
                else:
                    line.tob -= interval
            line.calc_fatigue(interval)




