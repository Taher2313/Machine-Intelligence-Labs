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

    def value(state, depth):

        # check if the state is terminal
        terminal, values = game.is_terminal(state)
        
        # if the state is terminal, return the state utility
        if terminal: return values[0] , None

        # if the depth is equal to the maximum depth, return the heuristic value
        if depth == max_depth: return heuristic(game, state, 0) , None

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
       

    # def solve_min_max(state, depth): 

    #     agent = game.get_turn(state)

    #     terminal, values = game.is_terminal(state)
        
    #     if terminal: return values[0] , None

    #     if depth == max_depth: return heuristic(game, state, 0) , None

    #     actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

    #     compare_value = -math.inf if agent == 0 else math.inf

    #     correct_action = None

    #     if agent == 0:
    #         for action , state in actions_states:
    #             min = solve_min_max(state, depth + 1)[0]
    #             if min > compare_value : compare_value ,correct_action = min , action
                
    #     else:
    #         for action , state in actions_states:
    #             max = solve_min_max(state, depth + 1)[0]
    #             if max <= compare_value: compare_value , correct_action = max , action
                
    #     return compare_value , correct_action
   
    # return solve_min_max(state, 0)
    return value(state, 0)


# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Write this function
    # NotImplemented()

    def solve_alpha_beta(state, depth, alpha, beta): 

        agent = game.get_turn(state)

        terminal, values = game.is_terminal(state)
        
        if terminal: return values[agent] , None

        if depth == max_depth: return heuristic(game, state, 0) , None

        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        compare_value = -math.inf if agent == 0 else math.inf

        correct_action = None

        if agent == 0:
            for action , state in actions_states:
                min_val = solve_alpha_beta(state, depth + 1, alpha, beta)[0]
                if min_val > compare_value : compare_value ,correct_action = min_val , action
                if compare_value >= beta: return compare_value , correct_action
                alpha = max(alpha, compare_value)                
        else:
            for action , state in actions_states:
                max_val = solve_alpha_beta(state, depth + 1, alpha, beta)[0]
                if max_val <= compare_value: compare_value , correct_action = max_val , action
                if compare_value <= alpha: return compare_value , correct_action
                beta = min(beta, compare_value)     
                
        return compare_value , correct_action

    return solve_alpha_beta(state, 0, -math.inf, math.inf)

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Write this function
    # NotImplemented()

    # def solve_alpha_beta_with_ordering(state, depth, alpha, beta): 

    #     agent = game.get_turn(state)

    #     terminal, values = game.is_terminal(state)
        
    #     if terminal: return values[agent] , None

    #     if depth == max_depth: return heuristic(game, state, 0) , None

    #     actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

    #     if agent == 0:
    #         # sort actions_states by heuristic value in descending order in a stable way
    #         actions_states.sort(key=lambda x: heuristic(game, x[1], 0), reverse=True)
    #     else:
    #         # sort actions_states by heuristic value in ascending order in a stable way
    #         actions_states.sort(key=lambda x: heuristic(game, x[1], 0))

    #     compare_value = -math.inf if agent == 0 else math.inf

    #     correct_action = None

    #     if agent == 0:
    #         for action , state in actions_states:
    #             min_val = solve_alpha_beta_with_ordering(state, depth + 1, alpha, beta)[0]
    #             if min_val > compare_value : compare_value ,correct_action = min_val , action
    #             if compare_value >= beta: return compare_value , correct_action
    #             alpha = max(alpha, compare_value)                
    #     else:
    #         for action , state in actions_states:
    #             max_val = solve_alpha_beta_with_ordering(state, depth + 1, alpha, beta)[0]
    #             if max_val <= compare_value: compare_value , correct_action = max_val , action
    #             if compare_value <= alpha: return compare_value , correct_action
    #             beta = min(beta, compare_value)     
                
    #     return compare_value , correct_action

    # return solve_alpha_beta_with_ordering(state, 0, -math.inf, math.inf)

    def solve_alpha_beta_with_ordering(state, depth, alpha, beta):
            
            agent = game.get_turn(state)
    
            terminal, values = game.is_terminal(state)
    
            if terminal: return values[0] , None
    
            if depth == max_depth: return heuristic(game, state, 0) , None
    
            actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    
            compare_value = -math.inf if agent == 0 else math.inf
    
            correct_action = None
    
            if agent == 0:
                # sort actions_states by heuristic value in descending order in a stable way
                actions_states.sort(key=lambda x: heuristic(game, x[1], 0), reverse=True)
                for action , state in actions_states:
                    min_val = solve_alpha_beta_with_ordering(state, depth + 1, alpha, beta)[0]
                    if min_val > compare_value : compare_value ,correct_action = min_val , action
                    if compare_value >= beta: return compare_value , correct_action
                    alpha = max(alpha, compare_value)                
            else:
                # sort actions_states by heuristic value in ascending order in a stable way
                actions_states.sort(key=lambda x: heuristic(game, x[1], 0))
                for action , state in actions_states:
                    max_val = solve_alpha_beta_with_ordering(state, depth + 1, alpha, beta)[0]
                    if max_val <= compare_value: compare_value , correct_action = max_val , action
                    if compare_value <= alpha: return compare_value , correct_action
                    beta = min(beta, compare_value)     
                    
            return compare_value , correct_action

    return solve_alpha_beta_with_ordering(state, 0, -math.inf, math.inf)

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Write this function
    # NotImplemented()

    def solve_expectimax(state, depth):
            
            agent = game.get_turn(state)
    
            terminal, values = game.is_terminal(state)
    
            if terminal: return values[0] , None
    
            if depth == max_depth: return heuristic(game, state, 0) , None
    
            actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    
            compare_value = -math.inf if agent == 0 else 0
    
            correct_action = None
    
            if agent == 0:
                for action , state in actions_states:
                    min_val = solve_expectimax(state, depth + 1)[0]
                    if min_val > compare_value : compare_value ,correct_action = min_val , action
            else:
                for action , state in actions_states:
                    max_val = solve_expectimax(state, depth + 1)[0]
                    compare_value += max_val / len(actions_states)
                    correct_action = action
                    
            return compare_value , correct_action

    return solve_expectimax(state, 0)