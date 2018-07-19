
class Player:

    def __init__(self, player_id, goal_differential, fatigue_level=1.0):
        """
        Player Constructor
        :param player_id: string, unique player identifier
        :param goal_differential: float, weighted goal differential stat
        :param fatigue_level: float [0,1], initial fatigue level, default: 1.0
        """
        self.id = player_id
        self.goal_differential = goal_differential
        self.fatigue_level = fatigue_level

    def __str__(self):
        return f"{self.id}: {self.goal_differential}, {self.fatigue_level}\n"

    def fatigue(self):
        # TODO: implement fatigue function
        print(f"    Player {self.id} fatigues")
        return

    def recover(self):
        # TODO: implement recover function
        print(f"    Player {self.id} recovers")
        return
