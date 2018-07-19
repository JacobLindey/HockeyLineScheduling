
class Team:
    def __init__(self, team_id, lines=None, starting_line_id=""):
        self.id = team_id

        if lines:
            self.lines = lines
        else:
            self.lines = {}

        self.current_line_id = starting_line_id

    def __str__(self):
        string = ""
        string += f"{self.id}: \n"

        for _, line in self.lines.items():
            string += "  " + str(line)

        return string

    def insert_line(self, line):
        self.lines[line.id] = line

    def handle_fatigue(self):
        # TODO: implement team wide fatigue handling
        print(f"Team {self.id} fatigues")
        return

    def swap_line(self):
        # TODO: implement line swapping
        print(f"Team {self.id} swaps lines")
        return
