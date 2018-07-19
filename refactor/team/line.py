
class Line:
    def __init__(self, line_id, players=None):
        """
        Line Constructor
        :param line_id: string, unique identifier for line
        :param players: dictionary, default=None
        """
        self.id = line_id

        if players:
            self.players = players
        else:
            self.players = {}

    def __str__(self):
        string = ""
        string += f"{self.id}: \n"

        for _, player in self.players.items():
            string += "    " + str(player)

        return string

    def insert_player(self, player):
        self.players[player.id] = player

    def insert_players(self, players):
        for player in players:
            self.insert_player(player)

    def fatigue(self):
        # TODO: implement line wide fatigue
        print(f"  Line {self.id} fatigues")
        return

    def recover(self):
        # TODO: implement line wide recover
        print(f"  Line {self.id} recovers")
        return
