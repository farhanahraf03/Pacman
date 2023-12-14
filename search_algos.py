import data_structures
import heapq

def dfs(problem):
    """
    Depth first graph search algorithm
    :param problem: representing the maze problem.
    :return: actions representing solutions to the problem
    or None if no solution
    """
    visited = set()
    stack = data_structures.Stack()
    state = problem.start_state()
    root = data_structures.Node(state, None, None)
    stack.push(root)
    while not stack.is_empty():
        node = stack.pop()
        if problem.is_goal(node.state):
            return node.solution()
        if node.state not in visited:
            visited.add(node.state)
            for child_state, action, action_cost in problem.expand(node.state):
                child_node = data_structures.Node(child_state, node, action)
                stack.push(child_node)
    return None

def bfs(problem):
    """
    Breadth first graph search algorithm
    :param problem representing the maze problem.
    :return: list of actions representing solutions to the problem
    or None if no solution
    """
    visited = set()
    stack = data_structures.Queue()
    state = problem.start_state()
    root = data_structures.Node(state, None, None)
    stack.push(root)
    while not stack.is_empty():
        node = stack.pop()
        if problem.is_goal(node.state):
            return node.solution()
        if node.state not in visited:
            visited.add(node.state)
            for child_state, action, action_cost in problem.expand(node.state):
                child_node = data_structures.Node(child_state, node, action)
                stack.push(child_node)
    return None

def ucs(problem):
    """
    Uniform cost first graph search algorithm
    :param problem representing the maze problem.
    :return: list of actions representing solutions to the problem
    or None if no solution
    """
    visited = set()
    stack = data_structures.PriorityQueue()
    state = problem.start_state()
    root = data_structures.Node(state, None, None, 0)  # adding initial cost
    stack.push(root, 0)

    while not stack.is_empty():
        node = stack.pop()

        if problem.is_goal(node.state):
            return node.solution()
        if node.state not in visited:
            visited.add(node.state)
            for child_state, action, action_cost in problem.expand(node.state):
                child_node = data_structures.Node(child_state, node,
                                                   action, node.total_cost + action_cost)
                stack.push(child_node, child_node.total_cost) # Push child node with its total cost

    return None