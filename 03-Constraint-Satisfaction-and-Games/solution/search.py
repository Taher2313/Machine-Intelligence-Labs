from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import math

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action


# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Write this function
    # NotImplemented()

    # get the turn of the player that starts the game
    orignal_turn = game.get_turn(state)

    def value(state, depth):

        # check if the state is terminal
        terminal, values = game.is_terminal(state)
        
        # if the state is terminal, return the state utility
        if terminal: return values[orignal_turn] , None

        # if the depth is equal to the maximum depth, return the heuristic value
        if depth == max_depth: return heuristic(game, state, orignal_turn) , None

        # get the current turn
        agent = game.get_turn(state)

        # if the current turn is 0, return the maximum value of the successors
        if agent == 0: return max_value(state, depth)

        # if the current turn is not 0, return the minimum value of the successors
        else: return min_value(state, depth)


    def min_value(state, depth):

        # get the actions and the successors of the state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # initialize the minimum value to infinity
        min_val = math.inf

        # initialize the correct action to None
        correct_action = None

        # loop through the actions and the successors
        for action , state in actions_states:

            # get the value of the successor
            successor_value = value(state, depth + 1)[0]

            # if the successor value is less than or equal the minimum value, update the minimum value and the correct action
            if successor_value <= min_val: min_val , correct_action = successor_value , action

        # return the minimum value and the correct action
        return min_val , correct_action     

    
    def max_value(state, depth):
        
        # get the actions and the successors of the state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # initialize the maximum value to negative infinity
        max_val = -math.inf

        # initialize the correct action to None
        correct_action = None

        # loop through the actions and the successors
        for action , state in actions_states:

            # get the value of the successor
            successor_value = value(state, depth + 1)[0]

            # if the successor value is greater than the maximum value, update the maximum value and the correct action
            if successor_value > max_val: max_val , correct_action = successor_value , action

        # return the maximum value and the correct action
        return max_val , correct_action


    return value(state, 0)


# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Write this function
    # NotImplemented()

    # get the turn of the player that starts the game
    orignal_turn = game.get_turn(state)
    
    def value(state, depth, alpha, beta):
            
        # check if the state is terminal
        terminal, values = game.is_terminal(state)
        
        # if the state is terminal, return the state utility
        if terminal: return values[orignal_turn] , None

        # if the depth is equal to the maximum depth, return the heuristic value
        if depth == max_depth: return heuristic(game, state, orignal_turn) , None

        # get the current turn
        agent = game.get_turn(state)

        # if the current turn is 0, return the maximum value of the successors
        if agent == 0: return max_value(state, depth, alpha, beta)

        # if the current turn is not 0, return the minimum value of the successors
        else: return min_value(state, depth, alpha, beta)


    def min_value(state, depth, alpha, beta):
            
        # get the actions and the successors of the state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # initialize the minimum value to infinity
        min_val = math.inf

        # initialize the correct action to None
        correct_action = None

        # loop through the actions and the successors
        for action , state in actions_states:

            # get the value of the successor
            successor_value = value(state, depth + 1, alpha, beta)[0]

            # if the successor value is less than or equal the minimum value, update the minimum value and the correct action
            if successor_value <= min_val: min_val , correct_action = successor_value , action

            # if the minimum value is less than or equal to the alpha, return the minimum value and the correct action
            # because the minimum value is less than or equal to the alpha
            # alpha is the best value that maximizer can guarantee along the current path of the search tree to the root
            # so if the minimum value is less than or equal to the alpha, the maximizer can guarantee that the minimum value is the best value
            # so there is no need to search further         
            if min_val <= alpha: return min_val , correct_action

            # update the beta value to the minimum of the beta and the minimum value 
            # so that the beta is the best value that the minimizer can guarantee along 
            # the current path of the search tree to the root
            beta = min(beta, min_val)

        # return the minimum value and the correct action
        return min_val , correct_action


    def max_value(state, depth, alpha, beta):
        
        # get the actions and the successors of the state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # initialize the maximum value to negative infinity
        max_val = -math.inf

        # initialize the correct action to None
        correct_action = None

        # loop through the actions and the successors
        for action , state in actions_states:

            # get the value of the successor
            successor_value = value(state, depth + 1, alpha, beta)[0]

            # if the successor value is greater than the maximum value, update the maximum value and the correct action
            if successor_value > max_val: max_val , correct_action = successor_value , action

            # if the maximum value is greater than or equal to the beta, return the maximum value and the correct action
            # because the maximum value is greater than or equal to the beta
            # beta is the best value that minimizer can guarantee along the current path of the search tree to the root
            # so if the maximum value is greater than or equal to the beta, the minimizer can guarantee that the maximum value is the best value
            # so there is no need to search further
            if max_val >= beta: return max_val , correct_action

            # update the alpha value to the maximum of the alpha and the maximum value
            # so that the alpha is the best value that the maximizer can guarantee along
            # the current path of the search tree to the root
            alpha = max(alpha, max_val)

        # return the maximum value and the correct action
        return max_val , correct_action
    

    return value(state, 0, -math.inf, math.inf)

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Write this function
    # NotImplemented()

    # get the turn of the player that starts the game
    orignal_turn = game.get_turn(state)

    def value(state, depth, alpha, beta):
                
        # check if the state is terminal
        terminal, values = game.is_terminal(state)
        
        # if the state is terminal, return the state utility
        if terminal: return values[orignal_turn] , None

        # if the depth is equal to the maximum depth, return the heuristic value
        if depth == max_depth: return heuristic(game, state, orignal_turn) , None

        # get the current turn
        agent = game.get_turn(state)

        # if the current turn is 0, return the maximum value of the successors
        if agent == 0: return max_value(state, depth, alpha, beta)

        # if the current turn is not 0, return the minimum value of the successors
        else: return min_value(state, depth, alpha, beta)

    
    def min_value(state, depth, alpha, beta):
                    
        # get the actions and the successors of the state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # sort actions_states by heuristic value in ascending order in a stable way
        actions_states.sort(key=lambda x: heuristic(game, x[1], 0))

        # initialize the minimum value to infinity
        min_val = math.inf

        # initialize the correct action to None
        correct_action = None

        # loop through the actions and the successors
        for action , state in actions_states:

            # get the value of the successor
            successor_value = value(state, depth + 1, alpha, beta)[0]

            # if the successor value is less than or equal the minimum value, update the minimum value and the correct action
            if successor_value <= min_val: min_val , correct_action = successor_value , action

            # if the minimum value is less than or equal to the alpha, return the minimum value and the correct action
            # because the minimum value is less than or equal to the alpha
            # alpha is the best value that maximizer can guarantee along the current path of the search tree to the root
            # so if the minimum value is less than or equal to the alpha, the maximizer can guarantee that the minimum value is the best value
            # so there is no need to search further         
            if min_val <= alpha: return min_val , correct_action

            # update the beta value to the minimum of the beta and the minimum value 
            # so that the beta is the best value that the minimizer can guarantee along 
            # the current path of the search tree to the root
            beta = min(beta, min_val)

        # return the minimum value and the correct action
        return min_val , correct_action

    def max_value(state, depth, alpha, beta):
            
        # get the actions and the successors of the state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # sort actions_states by heuristic value in descending order in a stable way
        actions_states.sort(key=lambda x: heuristic(game, x[1], 0), reverse=True)

        # initialize the maximum value to negative infinity
        max_val = -math.inf

        # initialize the correct action to None
        correct_action = None

        # loop through the actions and the successors
        for action , state in actions_states:

            # get the value of the successor
            successor_value = value(state, depth + 1, alpha, beta)[0]

            # if the successor value is greater than the maximum value, update the maximum value and the correct action
            if successor_value > max_val: max_val , correct_action = successor_value , action

            # if the maximum value is greater than or equal to the beta, return the maximum value and the correct action
            # because the maximum value is greater than or equal to the beta
            # beta is the best value that minimizer can guarantee along the current path of the search tree to the root
            # so if the maximum value is greater than or equal to the beta, the minimizer can guarantee that the maximum value is the best value
            # so there is no need to search further
            if max_val >= beta: return max_val , correct_action

            # update the alpha value to the maximum of the alpha and the maximum value
            # so that the alpha is the best value that the maximizer can guarantee along
            # the current path of the search tree to the root
            alpha = max(alpha, max_val)

        # return the maximum value and the correct action
        return max_val , correct_action 

    return value(state, 0, -math.inf, math.inf) 


# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Write this function
    # NotImplemented()

    # get the turn of the player that starts the game
    orignal_turn = game.get_turn(state)

    def value(state, depth):
                    
        # check if the state is terminal
        terminal, values = game.is_terminal(state)
        
        # if the state is terminal, return the state utility
        if terminal: return values[orignal_turn] , None

        # if the depth is equal to the maximum depth, return the heuristic value
        if depth == max_depth: return heuristic(game, state, orignal_turn) , None

        # get the current turn
        agent = game.get_turn(state)

        # if the current turn is 0, return the maximum value of the successors
        if agent == 0: return max_value(state, depth)

        # if the current turn is not 0, return the expected value of the successors
        else: return expected_value(state, depth)

    
    def expected_value(state, depth):
                        
            # get the actions and the successors of the state
            actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    
            # initialize the expected value to 0
            expected_val = 0

            # loop through the actions and the successors
            for _ , state in actions_states:
    
                # get the value of the successor
                successor_value = value(state, depth + 1)[0]
    
                # update the expected value by adding the successor value to the expected value
                expected_val += successor_value
    
            # return the expected value and the correct action
            return expected_val / len(actions_states) , None


    def max_value(state, depth):
                    
        # get the actions and the successors of the state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # initialize the maximum value to negative infinity
        max_val = -math.inf

        # initialize the correct action to None
        correct_action = None

        # loop through the actions and the successors
        for action , state in actions_states:

            # get the value of the successor
            successor_value = value(state, depth + 1)[0]

            # if the successor value is greater than the maximum value, update the maximum value and the correct action
            if successor_value > max_val: max_val , correct_action = successor_value , action

        # return the maximum value and the correct action
        return max_val , correct_action
    
    return value(state, 0)