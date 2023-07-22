from dungeon import DungeonProblem, DungeonState
from mathutils import Direction, Point, euclidean_distance, manhattan_distance
from helpers import utils

# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)

#TODO: Import any modules and write any functions you want to use

def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    #TODO: ADD YOUR CODE HERE
    #IMPORTANT: DO NOT USE "problem.is_goal" HERE.
    # Calling it here will mess up the tracking of the explored nodes count
    # which is considered the number of is_goal calls during the search
    #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
    # utils.NotImplemented()

    '''
    The nain idea is to cal the biggest distance between the player move in each direction
    this is a lower bound of the actual cost

    The min distance between in each axis is calculated twice taking into consideration the player move in a direction a come back    
    '''

    # if the player is at the exit and the coins are empty, then the cost is 0
    if state.player == problem.layout.exit and len(state.remaining_coins) == 0:
        return 0

    # get the x distance between the player and the most left coin if there is a 
    x_distance = 0
    if len(state.remaining_coins) > 0:
        x_distance = state.player.x - min(state.remaining_coins, key=lambda p: p.x).x
        if x_distance < 0:
            x_distance = 0

    # get the y distance between the player and the most top coin
    y_distance = 0
    if len(state.remaining_coins) > 0:
        y_distance = state.player.y - min(state.remaining_coins, key=lambda p: p.y).y
        if y_distance < 0:
            y_distance = 0

    # get the distance between the player and the most right coin
    x_distance2 = 0
    if len(state.remaining_coins) > 0:
        x_distance2 = max(state.remaining_coins, key=lambda p: p.x).x - state.player.x
        if x_distance2 < 0:
            x_distance2 = 0
    
    # get the distance between the player and the most bottom coin
    y_distance2 = 0
    if len(state.remaining_coins) > 0:
        y_distance2 = max(state.remaining_coins, key=lambda p: p.y).y - state.player.y
        if y_distance2 < 0:
            y_distance2 = 0
 
    return x_distance + y_distance + x_distance2 + y_distance2 + min(x_distance, x_distance2) + min(y_distance, y_distance2) 
  
  