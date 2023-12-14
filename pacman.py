"""
Main program to guide Pacman on a quest within a given maze

Usage:  pacman.py maze_file search_algorithm
The maze_file is a text file such as questA.txt
The search_algorithm is:
    dfs: for depth first search
    bfs: for breadth first search
    ucs for uniform cost search
Example:  pacman.py questA.txt dfs


"""
import time
import argparse
import search_algos
import graphics

class Maze(object):
    """
    Represents maze layout: width, height and walls

    Parameters:
    width (int):  the width of the maze
    height (int): the height of the maze
    wall_status (two dimensional list of booleans):
        With each elememt representing position in maze,
        True indicates presence of wall in the given position.
        False indicates the absence of a wall.
    """
    def __init__(self, width, height):
        self.wall_status = [[False for x in range(width)]
                      for y in range(height)]
        self.width = width
        self.height = height

    def add_wall(self, position):
        """
        Adds a wall in the given position
        :param position: represents (x, y) position of maze.
        :return: None
        """
        x, y = position
        self.wall_status[y][x] = True

    def is_wall(self, position):
        """
        checks if there a wall in the given position
        :param position: represents (x, y) position of maze.
        :return: (Boolean) True wall present in the position,
        False otherwise
        """
        x, y = position
        return self.wall_status[y][x]

    def within_maze(self, position):
        """
        checks if the given position within bounds
        :param position:  represents (x, y) position of maze.
        :return: (Boolean) True wall present in the position,
        False otherwise
        """
        x, y = position
        return (0 <= x <= self.width -1) and (0 <= y <= self.height - 1)


class Problem(object):
    """
    Parameters:
    mazefile: a text file containing the maze positions

    Attributes:
    maze: a maze problem given to solve.
    pacman_position: the current position of Pacman
    snack: a set of info for the positions of the
    remaining snack in the quest
    """
    directions = {"E": (1, 0), "W": (-1, 0), "S": (0, 1), "N": (0, -1)}

    # The cost associated with each move.
    cost = {"E": 1, "W": 1, "S": 1, "N": 1}

    def __init__(self, mazefile):
        self._nodes_expanded = 0 # private variable
        self.medals = set()
        self.read_quest(mazefile)

    def read_quest(self, mazefile):
        """
        Read maze from the text file and store info according to the lines.
        W or w:  represent a wall.
        M or m: represents medals.
        S or s: start position.
        Any other character: a vacant maze position
        :param
        mazefile (file object): tfile obj with maze info
        :return: None
        """
        area = mazefile.readlines()
        width = len(area[0].strip()) # the first line
        height = len(area) # the number of lines represents the height
        self.maze = Maze(width, height)
        y = 0
        for line in area:
            x = 0
            for char in line:
                if char in {'W', 'w'}:
                    self.maze.add_wall((x, y))
                elif char in {'M', 'm'}:
                    self.add_medal((x, y))
                elif char in {'S', 's'}:
                    self.set_pacman((x, y))
                x += 1
            y += 1
        mazefile.close()


    def set_pacman(self, position):
        """
        Save Pacman's position
        :param position: (x,y) representing position in maze.
        :return: None
        """
        self.pacman_position = position

    def add_medal(self, position):
        """
        Add the given position to the set containing medals
        :param position: tuple (x, y) representing a maze position
        :return: None
        """
        self.medals.add(position)

    def is_goal(self, state):
        """
        Goal state is when there are no medals left.
        :param
        state - current position (x,y)
        :return: Boolean - True if this is a goal state, False otherwise
        """
        position, medals_left = state
        return not medals_left

    def start_state(self):
        """
        Return the start state in the layout

        :return:
        state - The start state in the quest
        """
        return self.pacman_position, tuple(self.medals)

    def expand(self, state):
        """
        Return list of all reachable states from current state and their cost
        :param
        state - current position (x,y)
        :return:
        a list of  all reachable states from current state and
        action and their cost
        """
        result = []
        self._nodes_expanded += 1
        position, current_medals = state
        pos_x, pos_y = position
        for action in self.directions:
            new_pos = (pos_x + self.directions[action][0],
                            pos_y + self.directions[action][1])
            # if the move in that direction is valid
            if self.maze.within_maze(new_pos) and \
                not self.maze.is_wall(new_pos):
                new_medals = set(current_medals) - {new_pos}
                new_state = (new_pos, tuple(new_medals))
                result.append((new_state, action, self.cost[action]))
        return result


    def path_cost(self, actions):
        """
        Return the total cost of pacman cations/moves
        :param
        actions (list) - A list of actions/moves
        :return (int):  the total cost of these actions
        """
        return sum(self.cost[action] for action in actions)

    def nodes_expanded(self):
        return self._nodes_expanded


def parse_arguments():
    '''
    Parse and validate the command line arguments
    :return: mazefile and search algorithm
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('maze_file',
                        help='name of text file containing the maze info',
                        type=argparse.FileType('r')) # open the file
    parser.add_argument('search_algorithm',
                        help='dfs, bfs or ucs?',
                        choices=['dfs', 'bfs', 'ucs'])
    arguments = parser.parse_args()

    maze_file = arguments.maze_file
    search = arguments.search_algorithm
    return maze_file, search

def main():
    
    maze_file, search = parse_arguments()
    quest = Problem(maze_file)
    search_function = getattr(search_algos, search)
    start_time = time.time()
    solution = search_function(quest)
    time_elapsed = time.time() - start_time

    # Print some statistics
    if solution is not None:
        print('Path length: ', len(solution))
        #print('Carrots consumed: ', quest.path_cost(solution))
    else:
        print('The quest failed!')
    print(f'Number of nodes expanded: {quest.nodes_expanded():,}')
    print(f'Processing time: {time_elapsed:.4f}(sec)')

    graphics.Display(quest, solution)  # Visualize the solution


if __name__ == '__main__':
    main()