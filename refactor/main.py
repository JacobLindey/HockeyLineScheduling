from team import Team, Line, Player


def recursive_process(starting_node, max_depth):
    # TODO: Generate tree @ start to max_depth
    # TODO: Prune Starting Tree
    #
    # TODO: Iterate through leaves
    #   TODO: evaluate paths recursively, storing in look up table for later
    #
    # TODO: Iterate through paths
    #   TODO: find maximal path
    #
    # TODO: return maximal path
    return


def main():
    # TODO: Setup team object
    team = Team("PITT")
    line1 = Line("lead")
    players_1 = [
        Player("Crosby", 1.024),
        Player("Hagelin", 0.458),
        Player("Kessel", 0.876)
        ]
    line1.insert_players(players_1)
    team.insert_line(line1)
    print(team)

    # TODO: Generate Starting Tree
    # TODO: Traverse starting tree and prune invalid branches
    #   Mark valid/invalid paths with boolean value stored in node.data
    #
    # TODO: Construct list of leaves
    # TODO: Iterate through leaves and recursively determine their values, storing

    return


if __name__ == "__main__":
    main()
