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
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #obtain information on the current state of things.
        currentPosition = currentGameState.getPacmanPosition()

        #Check for the best or worst-case outcomes, as well as the highest score for a winning state.
        if successorGameState.isWin():
            return 99999

        #Worst case scenario: pacman and ghost are in the same place, but ghost is not afraid.
        for state in newGhostStates:
            if state.getPosition() == currentPosition and state.scaredTimer == 0:
                return -99999
        score = 0
        #to prevent pacman stopping because of an action that causes him to stop negative score
        if action == 'Stop':
            score -= 100
        #Check the distance of food from the Pacman to get a better score for states with food close by and ghosts far away.
        foodInterval = [util.manhattanDistance(newPos, food) for food in newFood]
        nearestFood = min(foodInterval)
        #Food that is closer to you should be given more weight - consider the opposite.
        score += float(1/nearestFood)
        #We want to select the state with the least amount of food remaining, so deduct the number of food left and proportional weight from this.
        score -= len(newFood)

        #Check the distance between the ghost's diet and the present and new states. If the condition is worse, subtract a point; otherwise, add a score for the current game state.
        currentGhostDistances = [util.manhattanDistance(newPos, ghost.getPosition()) for ghost in currentGameState.getGhostStates()]
        nearestCurrentGhost = min(currentGhostDistances)
        #for new GameStates
        newGhostDistances = [util.manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
        nearestNewGhost = min(newGhostDistances)

        #farther ghosts are good
        if nearestNewGhost < nearestCurrentGhost:
            score -= 100
        else:
            score += 200

        return successorGameState.getScore() + score


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


    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        #work with the smallest value
        def minValue(state, agentIndex, depth):
            #data on the number of agents and the index's legal behavior
            agentCount = gameState.getNumAgents()
            legalActions = state.getLegalActions(agentIndex)

            #If no legal steps are taken, the assessment function is restored.
            if not legalActions:
                return self.evaluationFunction(state)

            #After all of the ghost movement, Pacman is the last to pass.
            if agentIndex == agentCount - 1:
                miniValue =  min(maxValue(state.generateSuccessor(agentIndex, action),\
                agentIndex,  depth) for action in legalActions)
            else:
                miniValue = min(minValue(state.generateSuccessor(agentIndex, action),\
                agentIndex + 1, depth) for action in legalActions)

            return miniValue

        #Only pacman uses the maximum value function, so index is set to 0.
        def maxValue(state, agentIndex, depth):
            #details on the agent database and the index's legal behavior
            agentIndex = 0
            legalActions = state.getLegalActions(agentIndex)

            #If no legal steps are taken or the maximum depth is not reached in recursion, the evaluation function is returned.
            if not legalActions  or depth == self.depth:
                return self.evaluationFunction(state)

            maximumValue =  max(minValue(state.generateSuccessor(agentIndex, action), \
            agentIndex + 1, depth + 1) for action in legalActions)

            return maximumValue

        #Agent index 0 maximizes the best possible moves for the rootnode, that is the pacman.
        actions = gameState.getLegalActions(0)
        #Find all actions and their corresponding values, then return the action with the highest value.
        allActions = {}
        for action in actions:
            allActions[action] = minValue(gameState.generateSuccessor(0, action), 1, 1)

        return max(allActions, key=allActions.get)

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #work with the smallest value
        def minValue(state, agentIndex, depth, alpha, beta):
            #data on the number of agents and the index's legal behavior
            agentCount = gameState.getNumAgents()
            legalActions = state.getLegalActions(agentIndex)

            #If no legal steps are taken, the assessment function is restored.
            if not legalActions:
                return self.evaluationFunction(state)

            #track the value
            miniValue = 99999
            currentBeta = beta
            #After all of the ghost movement, Pacman is the last to pass.
            if agentIndex == agentCount - 1:
                for action in legalActions:
                    miniValue =  min(miniValue, maxValue(state.generateSuccessor(agentIndex, action), \
                    agentIndex,  depth, alpha, currentBeta))
                    if miniValue < alpha:
                        return miniValue
                    currentBeta = min(currentBeta, miniValue)

            else:
                for action in legalActions:
                    miniValue =  min(miniValue,minValue(state.generateSuccessor(agentIndex, action), \
                    agentIndex + 1, depth, alpha, currentBeta))
                    if miniValue < alpha:
                        return miniValue
                    currentBeta = min(currentBeta, miniValue)

            return miniValue

        #Only pacman uses the maximum value function, so index is set to 0.
        def maxValue(state, agentIndex, depth, alpha, beta):
            #details on the agent database and the index's legal behavior
            agentIndex = 0
            legalActions = state.getLegalActions(agentIndex)

            #If no legal steps are taken or the maximum depth is not reached in recursion, the evaluation function is returned.
            if not legalActions  or depth == self.depth:
                return self.evaluationFunction(state)

            #track the value
            maximumValue = -99999
            currentAlpha = alpha

            for action in legalActions:
                maximumValue = max(maximumValue, minValue(state.generateSuccessor(agentIndex, action), \
                agentIndex + 1, depth + 1, currentAlpha, beta) )
                if maximumValue > beta:
                    return maximumValue
                currentAlpha = max(currentAlpha, maximumValue)
            return maximumValue

        #Agent index 0 maximizes the best possible moves for the rootnode, which is the pacman. Obtain state information and set alpha and beta values
        actions = gameState.getLegalActions(0)
        alpha = -99999
        beta = 99999
        #Find all actions and their corresponding values, then return the action with the highest value.
        allActions = {}
        for action in actions:
            value = minValue(gameState.generateSuccessor(0, action), 1, 1, alpha, beta)
            allActions[action] = value

            #a new alpha
            if value > beta:
                return action
            alpha = max(value, alpha)

        return max(allActions, key=allActions.get)

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """


    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        #role of expected value
        def expValue(state, agentIndex, depth):
            #data on the number of agents and the index's legal behavior
            agentCount = gameState.getNumAgents()
            legalActions = state.getLegalActions(agentIndex)

            #If no legal steps are taken, the assessment function is restored.
            if not legalActions:
                return self.evaluationFunction(state)

            #the likelihood and the predicted value
            expectedValue = 0
            probabilty = 1.0 / len(legalActions)
            #After all of the ghost movement, Pacman is the last to pass.
            for action in legalActions:
                if agentIndex == agentCount - 1:
                    currentExpValue =  maxValue(state.generateSuccessor(agentIndex, action), \
                    agentIndex,  depth)
                else:
                    currentExpValue = expValue(state.generateSuccessor(agentIndex, action), \
                    agentIndex + 1, depth)
                expectedValue += currentExpValue * probabilty

            return expectedValue


        #Only pacman uses the maximum value function, so index is set to 0.
        def maxValue(state, agentIndex, depth):
            #details on the agent database and the index's legal behavior
            agentIndex = 0
            legalActions = state.getLegalActions(agentIndex)

            #If no legal steps are taken or the maximum depth is not reached in recursion, the evaluation function is returned.
            if not legalActions  or depth == self.depth:
                return self.evaluationFunction(state)

            maximumValue =  max(expValue(state.generateSuccessor(agentIndex, action), \
            agentIndex + 1, depth + 1) for action in legalActions)

            return maximumValue

        #Agent index 0 maximizes the best possible moves for the rootnode, which is the pacman.
        actions = gameState.getLegalActions(0)
        #Find all actions and their corresponding values, then return the action with the highest value.
        allActions = {}
        for action in actions:
            allActions[action] = expValue(gameState.generateSuccessor(0, action), 1, 1)

        #returning the operation with the highest predicted value
        return max(allActions, key=allActions.get)

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
   Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    # Useful information you can extract from a GameState pacman.py
    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood().asList()
    currentGhostStates = currentGameState.getGhostStates()
    currentScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]
    currentCapsule = currentGameState.getCapsules()
    #best ranking for a state that has won
    if currentGameState.isWin():
        return 99999

    #In the worst-case scenario, pacman and the ghost are in the same place but the ghost isn't afraid.
    for state in currentGhostStates:
        if state.getPosition() == currentPos and state.scaredTimer == 1:
            return -99999

    score = 0

    #food gobbling higher score for states with food close by and ghosts far away, check the distance of food from the Pacman
    foodInterval = [util.manhattanDistance(currentPos, food) \
    for food in currentFood]
    nearestFood = min(foodInterval)
    #Food that is closer to you should be given more weight consider the opposite.
    score += float(1/nearestFood)
    #We want to select the state with the least amount of food remaining, so deduct the number of food left and proportional weight from this.
    score -= len(currentFood)

    #chase capsule score for catching pellets in capsules
    if currentCapsule:
        capsuleInterval = [util.manhattanDistance(currentPos, capsule) \
        for capsule in currentCapsule]
        nearestCapsule = min(capsuleInterval)
        #better if you're near a capsule
        score += float(1/nearestCapsule)

    #If the ghost is afraid, chase it; otherwise, stop it
    currentGhostInterval = [util.manhattanDistance(currentPos, ghost.getPosition()) \
    for ghost in currentGameState.getGhostStates()]
    nearestCurrentGhost = min(currentGhostInterval)
    scaredTime = sum(currentScaredTimes)
    #farther ghosts are good
    if nearestCurrentGhost >= 1:
        if scaredTime < 0:
            score -= 1/nearestCurrentGhost
        else:
            score += 1/nearestCurrentGhost

    return currentGameState.getScore() + score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction