# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        food_distances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        min_food_distance = min(food_distances) if food_distances else 1

        ghost_distances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
        min_ghost_distance = min(ghost_distances) if ghost_distances else 0

        score = successorGameState.getScore() - min_food_distance + (0.5* min_ghost_distance)
        if action == "Stop":
            score = -99999999999
        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def minimax(self, gameState, agentIndex, depth):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            option = Directions.STOP, self.evaluationFunction(gameState)
            #return option
        elif agentIndex == 0:
            agentIndex += 1
            option = self.maximizer(gameState, agentIndex, depth)
        else:
            if agentIndex == gameState.getNumAgents() -1:
                agentIndex = 0
                depth = depth - 1
            else:
                agentIndex += 1
            option = self.minimizer(gameState, agentIndex, depth)
            
        return option

    def maximizer(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose():
            return Directions.STOP, self.evaluationFunction(gameState)
        maximum = -999999999999999999
        action_legal = gameState.getLegalActions(0)
        for action in action_legal:
            temp_list = self.minimax(gameState.generateSuccessor(0, action), agentIndex, depth)
            temp_score = temp_list[1]
            if temp_score > maximum:
                maximum = temp_score
                curr_action = action
        return_tup = (curr_action, maximum)
        return return_tup
    
    def minimizer(self, gameState, agentIndex, depth):
        
        if gameState.isWin() or gameState.isLose():
            return Directions.STOP, self.evaluationFunction(gameState)
        if agentIndex == 0:
            temp_index = gameState.getNumAgents()-1
        else:
            temp_index = agentIndex-1
        minimum = 999999999999999
        action_legal = gameState.getLegalActions(temp_index)
        # for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
        #     x,y = state[0]
        for action in action_legal:
            temp_list = self.minimax(gameState.generateSuccessor(temp_index, action), agentIndex, depth)
            temp_score = temp_list[1]
            if temp_score < minimum:
                minimum =  temp_score
                curr_action = action
        return_tup = (curr_action, minimum)
        return return_tup


    def getAction(self, gameState):
#         """
#         Returns the minimax action from the current gameState using self.depth
#         and self.evaluationFunction.

#         Here are some method calls that might be useful when implementing minimax.

#         gameState.getLegalActions(agentIndex):
#         Returns a list of legal actions for an agent
#         agentIndex=0 means Pacman, ghosts are >= 1

#         gameState.generateSuccessor(agentIndex, action):
#         Returns the successor game state after an agent takes an action

#         gameState.getNumAgents():
#         Returns the total number of agents in the game

#         gameState.isWin():
#         Returns whether or not the game state is a winning state

#         gameState.isLose():
#         Returns whether or not the game state is a losing state
#         """
#         "*** YOUR CODE HERE ***"
    
        temp_list = self.minimax(gameState, 0, self.depth)
        # print(temp_list[0])
        return temp_list[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def minimax(self, gameState, agentIndex, depth, a, b):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            option = Directions.STOP, self.evaluationFunction(gameState)
            #return option
        elif agentIndex == 0:
            agentIndex += 1
            option = self.maximizer(gameState, agentIndex, depth, a, b)
        else:
            if agentIndex == gameState.getNumAgents() -1:
                agentIndex = 0
                depth = depth - 1
            else:
                agentIndex += 1
            option = self.minimizer(gameState, agentIndex, depth, a, b)
            
        return option

    def maximizer(self, gameState, agentIndex, depth, a, b):
        if gameState.isWin() or gameState.isLose():
            return Directions.STOP, self.evaluationFunction(gameState)
        maximum = -999999999999999999
        action_legal = gameState.getLegalActions(0)
        for action in action_legal:
            temp_list = self.minimax(gameState.generateSuccessor(0, action), agentIndex, depth, a, b)
            temp_score = temp_list[1]
            if temp_score > maximum:
                maximum = temp_score
                curr_action = action
            if temp_score > b:
                return_tup = (curr_action, maximum)
                # a = max(a, temp_score)
                return return_tup
            a = max(a, temp_score)
        return_tup = (curr_action, maximum)
        return return_tup
    
    def minimizer(self, gameState, agentIndex, depth, a, b):
        
        if gameState.isWin() or gameState.isLose():
            return Directions.STOP, self.evaluationFunction(gameState)
        if agentIndex == 0:
            temp_index = gameState.getNumAgents()-1
        else:
            temp_index = agentIndex-1
        minimum = 999999999999999
        action_legal = gameState.getLegalActions(temp_index)
        # for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
        #     x,y = state[0]
        for action in action_legal:
            temp_list = self.minimax(gameState.generateSuccessor(temp_index, action), agentIndex, depth, a, b)
            temp_score = temp_list[1]
            if temp_score < minimum:
                minimum =  temp_score
                curr_action = action
            if temp_score < a:
                return_tup = (curr_action, minimum)
                return return_tup
            b = min(b, temp_score)
        return_tup = (curr_action, minimum)
        return return_tup


    def getAction(self, gameState):
#         """
#         Returns the minimax action from the current gameState using self.depth
#         and self.evaluationFunction.

#         Here are some method calls that might be useful when implementing minimax.

#         gameState.getLegalActions(agentIndex):
#         Returns a list of legal actions for an agent
#         agentIndex=0 means Pacman, ghosts are >= 1

#         gameState.generateSuccessor(agentIndex, action):
#         Returns the successor game state after an agent takes an action

#         gameState.getNumAgents():
#         Returns the total number of agents in the game

#         gameState.isWin():
#         Returns whether or not the game state is a winning state

#         gameState.isLose():
#         Returns whether or not the game state is a losing state
#         """
#         "*** YOUR CODE HERE ***"
    
        temp_list = self.minimax(gameState, 0, self.depth, -999999, 999999)
        # print(temp_list[0])
        return temp_list[0]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        def max_value(state, depth):
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            v = 0
            for action in state.getLegalActions(0):
                v = max(v, expect_value(state.generateSuccessor(0, action), depth, 1))
            return v

        def expect_value(state, depth, ghost_index):
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            v = 0
            for action in state.getLegalActions(ghost_index):
                if ghost_index == state.getNumAgents() - 1:
                    v += max_value(state.generateSuccessor(ghost_index, action), depth - 1)
                else:
                    v += expect_value(state.generateSuccessor(ghost_index, action), depth, ghost_index + 1)
            return v / len(state.getLegalActions(ghost_index))

        actions = gameState.getLegalActions(0)
        values = [expect_value(gameState.generateSuccessor(0, action), self.depth, 1) for action in actions]
        best_action_index = values.index(max(values))
        return actions[best_action_index]
    

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    successorGameState = currentGameState

    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    food_distances = [manhattanDistance(newPos, food) for food in newFood.asList()]
    min_food_distance = min(food_distances) if food_distances else 1

    ghost_distances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
    min_ghost_distance = min(ghost_distances) if ghost_distances else 0

    score = successorGameState.getScore() - min_food_distance
    """
    if action == "Stop":
        score = -99999999999
    """
    return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
