"""
Class definitions for data structures used by the search algorithms
"""
import heapq

class Node(object):

    def __init__(self, state, parent, action, total_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.total_cost = total_cost  # cost from root

    def solution(self):
        """
        Returns sequence of moves from the root to current node
        :return: list of actions
        """
        return [node.action for node in self._node_path()[1:]]

    def _node_path(self):
        """
        Returns list of nodes from the root to current node.
        :return: list of Node objects
        """
        node = self
        path = []
        while node:
            path.append(node)
            node = node.parent
        path.reverse()
        return path


class Stack(object):
    """
    Stack with LIFO (last in first out) queuing
    """

    def __init__(self):
        self.list = []

    def push(self, item):
        self.list.append(item)

    def pop(self):
        return self.list.pop()

    def is_empty(self):
        return not self.list


class Queue:
    """
    Represents queue with FIFO (first in first out) queuing
    """

    def __init__(self):
        self.list = []

    def push(self, item):
        self.list.insert(0, item)

    def pop(self):
        return self.list.pop()

    def is_empty(self):
        return not self.list


class PriorityQueue(object):
    """
    Represents a priority queue.
    """

    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        priority, count, item = heapq.heappop(self.heap)
        return item

    def is_empty(self):
        return not self.heap
