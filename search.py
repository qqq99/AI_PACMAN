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
    A sample depth first search implementation is provided for you to help you understand how to interact with the problem.
    """
    mystack = util.Stack()
    startState = (problem.getStartState(), '', 0, [])
    mystack.push(startState)
    visited = set()
    while mystack :
        state = mystack.pop()
        node, action, cost, path = state
        if node not in visited :
            visited.add(node)
            if problem.isGoalState(node) :
                path = path + [(node, action)]
                break;
            succStates = problem.getSuccessors(node)
            for succState in succStates :
                succNode, succAction, succCost = succState
                newstate = (succNode, succAction, cost + succCost, path + [(node, action)])
                mystack.push(newstate)
    actions = [action[1] for action in path]
    del actions[0]
    return actions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    myqueue = util.Queue()
    startState = (problem.getStartState(), '', 0, [])
    myqueue.push(startState)
    visited = set()
    while myqueue:
        state = myqueue.pop()
        node, action, cost, path = state
        if node not in visited:
            visited.add(node)
            if problem.isGoalState(node):
                path = path + [(node, action)]
                break;
            succStates = problem.getSuccessors(node)
            for succState in succStates:
                succNode, succAction, succCost = succState
                newstate = (succNode, succAction, cost + succCost, path + [(node, action)])
                myqueue.push(newstate)
    actions = [action[1] for action in path]
    del actions[0]
    return actions


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    myPriorityQueue = util.PriorityQueueWithFunction(lambda x: x[2])
    startState = (problem.getStartState(), '', 0, [])
    myPriorityQueue.push(startState)
    visited = set()
    while myPriorityQueue:
        state = myPriorityQueue.pop()
        node, action, cost, path = state
        if node not in visited:
            visited.add(node)
            if problem.isGoalState(node):
                path = path + [(node, action)]
                break;
            succStates = problem.getSuccessors(node)
            for succState in succStates:
                succNode, succAction, succCost = succState
                newstate = (succNode, succAction, cost + succCost, path + [(node, action)])
                myPriorityQueue.push(newstate)
    actions = [action[1] for action in path]
    del actions[0]
    return actions
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    myPriorityqueue = util.PriorityQueue()
    myPriorityqueue.push((problem.getStartState(),[],0),0+ heuristic(problem.getStartState(),problem))
    visited = set()
    while not myPriorityqueue.isEmpty():
        state = myPriorityqueue.pop()
        node, path, gcost = state
        if node not in visited:
            visited.add(node)
            if problem.isGoalState(node):
                return path
            succStates = problem.getSuccessors(node)
            for succState in succStates:
                succNode, succAction, succCost = succState
                cost = (gcost + succCost) + heuristic(succNode,problem)
                myPriorityqueue.push((succNode, path +[succAction], (gcost+succCost)),cost)
    return []

def enforcedHillClimbing(problem, heuristic=nullHeuristic):
    """COMP90054 your solution to part 1 here """
    startNode = problem.getStartState()
    startState = (startNode,[], heuristic(startNode, problem))
    def improve(problem, currentNodeState, heuristic=nullHeuristic):
        myqueue = util.Queue()
        myqueue.push(currentNodeState)
        visited = set()
        while not myqueue.isEmpty():
            state = myqueue.pop()
            node, path,h = state
            if node not in visited:
                visited.add(node)
                if h < currentNodeState[2]:
                    return state
                succStates = problem.getSuccessors(node)
                for succNode, succAction, succCost in succStates:
                    newPath = path +[succAction]
                    newH = heuristic(succNode,problem)
                    succState =(succNode,newPath,newH)
                    myqueue.push(succState)
        return None
    while not problem.isGoalState(startState[0]):
        if startState is None:
            return []
        startState = improve(problem, startState, heuristic)
    return startState[1]
    
def idaStarSearch(problem, heuristic=nullHeuristic):
    """COMP90054 your solution to part 2 here """
    bound = heuristic(problem.getStartState(), problem)
    while True:
        myPriorityqueue = util.PriorityQueue()
        myPriorityqueue.push((problem.getStartState(), [], 0), 0 + heuristic(problem.getStartState(), problem))
        visited = set()
        #startState = problem.getStartState()
        minCost = 99999999999
        while not myPriorityqueue.isEmpty():
            state = myPriorityqueue.pop()
            node, path, gcost = state
            if node not in visited:
                visited.add(node)
                if problem.isGoalState(node):
                    return path
                if gcost + heuristic(node,problem) <= bound:
                    succStates = problem.getSuccessors(node)
                    for succState in succStates:
                        succNode, succAction, succCost = succState
                        if succNode not in visited:
                            newCost = (gcost + succCost) + heuristic(succNode, problem)
                            myPriorityqueue.push((succNode, path + [succAction], gcost + succCost),newCost)
                else:
                    if gcost + heuristic(node,problem) < minCost:
                        minCost = gcost + heuristic(node,problem)
        bound = minCost

                
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ehc = enforcedHillClimbing
ida = idaStarSearch