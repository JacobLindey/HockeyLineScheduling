from Team import Team
from Line import Line
from Path import Path
from CONSTANTS import *
import sys
import time


def theoretical_nodes(depth):
    return int(4/3*(4**depth-1))


def prune_tree(tree):
    """
    removes elements from tree that do not meet requirements
    :param tree: the unpruned tree
    :return: pruned tree
    """
    # collect the nodes that need removed
    to_remove = []
    for child in tree:
        if child.toi > 0:
            tree = [child]
            return tree
        else:
            if child.tob > 0:
                to_remove.append(child)

    # remove the nodes
    for item in to_remove:
        tree.remove(item)

    # return the pruned tree
    return tree


def construct_tree(path):
    """
    creates the child tree based on the path, simply each line that is considered
    :param path: the current path which contains the team information
    :return: list containing the lines for consideration
    """
    return [child for child in path.team.lines]


def process(node, path, depth, max_depth):
    """
    recursive function that navigates a generated tree with root node to a max layer depth of depth
    :param node: the root node, current line on ice
    :param path: the current path being explored, also contains team information
    :param depth: the current depth of the node from the original root
    :param max_depth:
    :return:
    """

    num_visited = 0

    # add the current root to the sequence and swap the curr_line num
    path.team.update(node, INTERVAL)
    path.add(path.team.lines[path.team.curr_line_index])

    # check end condition
    if depth >= max_depth:
        # evaluate the score for the path and return to parent node
        path.evaluate()
        return path, 1

    # construct the one layer tree and prune
    tree = construct_tree(path)
    tree = prune_tree(tree)

    # investigate the paths that lead from each child, recursive step
    child_paths = []
    for child in tree:

        temp_path = path.copy()
        # investigate child paths
        max_path, num_v = process(child, temp_path, depth + 1, max_depth)
        child_paths.append(max_path)  # add the maximal path received from the child

        num_visited += 1
        num_visited += num_v

    # attempt to find the max value child path
    try:  # this try statement is in case of error, i.e. there should be no case where this throws exception
        maximum_path = child_paths[0]

    except IndexError:
        '''
            * This is only caught in the case of complete fault.
            * In this case, check th pruning function. It may be
            * excluding too many nodes.
        '''
        print("Child_Paths empty")
        sys.exit(1)

    # continue to find maximal child path
    for i in range(1, len(child_paths)):
        try:
            if child_paths[i].value > maximum_path.value:
                maximum_path = child_paths[i]

        except IndexError:
            print("Index out of domain at depth " + str(depth) + " index " + str(i))
            sys.exit(1)

    # return the maximal child path
    return maximum_path, num_visited


def main():
    """
    Sets up and processes team, EXAMPLE;
    :return: NONE
    """
    # Setup Team Object
    team_edm = Team()
    lines = list()
    lines.append(Line(0, 1.701))
    lines.append(Line(1, 0.658))
    lines.append(Line(2, 0.299))
    lines.append(Line(3, 0.433))
    team_edm.set_team("EDM", lines=lines, start_line_index=0)  # Edmonton Oilers

    print(team_edm)

    # Setup Path Object
    path = Path()
    path.team = team_edm

    schedule = []
    num_intervals = PERIOD_LENGTH // INTERVAL
    start = time.time()
    for i in range(num_intervals - 1):

        max_depth = MAX_DEPTH
        if num_intervals - i < MAX_DEPTH:
            max_depth = num_intervals - i

        # start = time.time()
        # find optimal path from curr_line for the next (MAX_DEPTH * INTERVAL) seconds
        temp_path = path.copy()
        optimal_path, num_visited = process(team_edm[team_edm.curr_line_index], temp_path, 1, max_depth)

        # print("\n\n", path.team, "\n\n")
        path.team.update(optimal_path[1], INTERVAL)
        schedule.append(optimal_path[1].line_num)
        elapsed_time = time.time() - start

        t_nodes = theoretical_nodes(max_depth)

        # print("Optimal       ", optimal_path)
        #
        print("Progress:     {p:3.0f}% @ t: {e:5.2f}".format(p=i/(num_intervals-1)*100, e=elapsed_time))
        # print("Look Ahead:   ", LOOK_AHEAD)
        # print("Depth:        ", max_depth)
        # print("Visited:      ", num_visited)
        # print("Theoretical:  ", t_nodes)
        # print("Removal Rate: ", "{0:0.5f}".format((t_nodes - num_visited)/t_nodes))
        # print("Speed Up:     ", "{0:4.2f}".format(t_nodes/num_visited))
        #
        # print("\nTime:       ", elapsed_time)

    print(schedule)


def pruning_test():
    # Setup Team Object
    team_edm = Team()
    lines = list()
    lines.append(Line(0, 1.701))
    lines.append(Line(1, 0.658))
    lines.append(Line(2, 0.299))
    lines.append(Line(3, 0.433))
    team_edm.set_team("EDM", lines=lines, start_line_index=0)  # Edmonton Oilers

    path = Path()
    path.team = team_edm

    values_best = []
    for i in range(30):
        temp_path = path.copy()
        optimal_path, num_visited = process(team_edm[team_edm.curr_line_index], temp_path, 1, i)
        values_best.append(num_visited)

    path.team[path.team.curr_line_index].toi = 0
    values_worst = []
    for i in range(30):
        temp_path = path.copy()
        optimal_path, num_visited = process(team_edm[team_edm.curr_line_index], temp_path, 1, i)
        values_worst.append(num_visited)

    theoretical_values = [theoretical_nodes(i) for i in range(30)]
    print(theoretical_values)
    print(values_best)
    print(values_worst)


if __name__ == "__main__":
    # pruning_test()
    main()
