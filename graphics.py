import tkinter

class Display(object):
    """
    Visualization of a given solution to a quest

    Params:
    problem: Representing a maze problem
    solution:  actions that are solutions to maze problem.

    canvas:  tkinter widget used to display/visualize the solution
    medal_rem: icons representing remaining medals
    pac: The pacman icon

    """
    time_interval = 90 
    size = 30  # pixel size

    def __init__(self, problem, solution):
        self.medal_rem = {}
        self.problem = problem
        root = tkinter.Tk()
        root.title('Pacman')
        self.canvas = tkinter.Canvas(root,
                                     width=self.size * problem.maze.width,
                                     height=self.size * problem.maze.height)
        self.canvas.grid()
        x_pos, y_pos = problem.pacman_position

        for y in range(problem.maze.height):
            for x in range(problem.maze.width):
                if problem.maze.is_wall((x, y)):
                    color = 'blue'
                else:
                    color = 'black'
                self.canvas.create_rectangle(x * self.size,
                                             y * self.size,
                                             (x + 1) * self.size,
                                             (y + 1) * self.size,
                                             fill=color,
                                             outline="")

        sammy = tkinter.PhotoImage(file='Pacman.png')

        self.pac = self.canvas.create_image((x_pos + 0.5) * self.size,
                                               (y_pos + 0.5) * self.size,
                                               image=sammy)
        for medal_x, medal_y in problem.medals:
            self.medal_rem[(medal_x, medal_y)] = \
                self.canvas.create_oval((medal_x + 0.25) * self.size,
                                        (medal_y + 0.25) * self.size,
                                        (medal_x + 0.75) * self.size,
                                        (medal_y + 0.75) * self.size,
                                        fill="gold",
                                        outline="")

        if solution is not None:
            self.actions = iter(solution)
            self.canvas.after(self.time_interval, self.move)
#            self.animate()
        root.mainloop()

    def animate(self):
        """
        Invoke the move method after the time interval.
        :return: None
        """
        self.canvas.after(self.time_interval, self.move)

    def move(self):
        """
        Move pacman according to action and schedule next move
        :return: None
        """
        try:
            action = next(self.actions)
        except StopIteration:
            return
        else:
            x, y = self.problem.pacman_position
            new_x = x + self.problem.directions[action][0]
            new_y = y + self.problem.directions[action][1]
            position = (new_x, new_y)

            if not self.problem.maze.within_maze(position):
                raise Exception('Falling off the maze....')
            elif self.problem.maze.is_wall(position):
                raise Exception('Crash!  Wall encountered')
            elif position in self.problem.medals:
                self.problem.medals.discard(position)
                self.canvas.itemconfigure(self.medal_rem[position],
                                          fill="")
            self.problem.pacman_position = position

            move_x, move_y = self.problem.directions[action]
            self.canvas.move(self.pac,
                             move_x * self.size,
                             move_y * self.size)
            self.canvas.create_line((x + 0.5) * self.size,
                                    (y + 0.5) * self.size,
                                    (new_x + 0.5) * self.size,
                                    (new_y + 0.5) * self.size,
                                    arrow = tkinter.LAST,
                                    width = 3,
                                    fill = "white")

            self.canvas.after(self.time_interval, self.move)
