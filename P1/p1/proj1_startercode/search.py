# Students: Rishi Mullangi and Sashwat Venkatesh

# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Stack()
    visited = []
    start_state = problem.getStartState()
    fringe.push(start_state)
    fringe.push([])
    
    while not fringe.isEmpty():
        path = fringe.pop()
        curr_state = fringe.pop()
        if curr_state not in visited:
            visited.append(curr_state)

            if problem.isGoalState(curr_state):
                return path

            for successor in problem.getSuccessors(curr_state):
                fringe.push(successor[0])
                fringe.push(path + [successor[1]])
    return []

def genericSearch(problem, queue):
    nodes = []
    queue = util.Queue()
    start = problem.getStartState()
    queue.push(start)
    queue.push([])
    # queue.push((start, []))
    while not queue.isEmpty():
        current = queue.pop()
        path = queue.pop()
        # current, path = queue.pop()
        if current not in nodes:
            nodes.append(current)
            if problem.isGoalState(current):
                return path
            for successor in problem.getSuccessors(current):
                queue.push(successor[0])
                queue.push(path + [successor[1]])
                # queue.push((successor[0], path + [successor[1]]))
    return []
    

def breadthFirstSearch(problem):
    return genericSearch(problem, util.Queue())
    # nodes = []
    # queue = util.Queue()
    # start = problem.getStartState()
    # queue.push(start)
    # queue.push([])
    # # queue.push((start, []))
    # while not queue.isEmpty():
    #     current = queue.pop()
    #     path = queue.pop()
    #     # current, path = queue.pop()
    #     if current not in nodes:
    #         nodes.append(current)
    #         if problem.isGoalState(current):
    #             return path
    #         for successor in problem.getSuccessors(current):
    #             queue.push(successor[0])
    #             queue.push(path + [successor[1]])
    #             # queue.push((successor[0], path + [successor[1]]))
    # return []
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    visited = []
    start_state = problem.getStartState()
    # fringe.push(start_state, 0)
    # fringe.push([], 0)
    fringe.push((start_state, []), 0)
    while not fringe.isEmpty():
        # curr_state = fringe.pop()
        # path = fringe.pop()
        curr_state, path = fringe.pop()
        
        
        if curr_state not in visited:
            visited.append(curr_state)           
            if problem.isGoalState(curr_state):
                return path
            for successor in problem.getSuccessors(curr_state):
                # fringe.push(successor[0], len(path))
                # fringe.push(path + [successor[1]], len(path))
                fringe.push((successor[0], path + [successor[1]]), problem.getCostOfActions(path) + successor[2])
    return []
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    visited = []
    start_state = problem.getStartState()
    # fringe.push(start_state, 0)
    # fringe.push([], 0)
    fringe.push((start_state, []), 0)
    while not fringe.isEmpty():
        # curr_state = fringe.pop()
        # path = fringe.pop()
        curr_state, path = fringe.pop()
        if curr_state not in visited:
            if problem.isGoalState(curr_state):
                return path
            visited.append(curr_state)
            for successor in problem.getSuccessors(curr_state):
                # fringe.push(successor[0], len(path) + heuristic(successor[0], problem))
                # fringe.push(path + [successor[1]], len(path) + heuristic(successor[0], problem))
                fringe.push((successor[0], path + [successor[1]]), problem.getCostOfActions(path) + successor[2] + heuristic(successor[0], problem))
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
