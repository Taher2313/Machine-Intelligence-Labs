from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers import utils
import heapq
#TODO: Import any modules you want to use

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()
    
    '''
        1.What the algorithm does :
            the algorithm uses a queue to keep track of the frontier
            The algorithm starts by adding the initial state to the frontier and the explored set.
            Then it loops until the frontier is empty.
            In each iteration the algorithm pops the first state from the frontier which is the first state added to the frontier and checks if it is the goal state.
            If it is the goal state it returns the path.
            If it is not the goal state the algorithm loops over all the possible actions in the current state.

        2.The data structure used : Queue

        3.Why this data structure is used :
            The data structure is used because it is a FIFO data structure and it is suitable for BFS.   
    '''

    # create a set to keep track of explored states
    explored = set()

    # create a queue to keep track of the frontier 
    frontier = deque()

    # add the initial state to the frontier with an empty path
    frontier.append((initial_state , []))
    
    # loop until the frontier is empty
    while frontier :

        # pop the first state from the frontier
        state , path  = frontier.popleft()

        # if the state is the goal state return the path
        if problem.is_goal(state):
            return path

        # add the state to the explored set
        explored.add(state)

        # loop over all the possible actions in the current state
        for action in problem.get_actions(state):

            # get the successors
            successor = problem.get_successor(state , action)

            # check if the successor is not in the explored set and not in the frontier
            if successor not in explored and successor not in [x[0] for x in frontier]:

                # create a new path by appending the current action to the current path
                new_path = list(path)
                new_path.append(action)

                # add the successor to the frontier with the new path
                frontier.append((successor , new_path)) 

    # if the frontier is empty and the goal state is not found return None
    # this means that there is no solution                      
    return None   

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()

    ''' 
        1.What the algorithm does : 
            the algorithm uses a stack to keep track of the frontier
            The algorithm starts by adding the initial state to the frontier and the explored set. 
            Then it loops until the frontier is empty.
            In each iteration the algorithm pops the first state from the frontier which is the last state added to the frontier and checks if it is the goal state.
            If it is the goal state it returns the path.
            If it is not the goal state the algorithm loops over all the possible actions in the current state.
            
        2.The data structure used : Stack

        3.Why this data structure is used :
            The data structure is used because it is a LIFO data structure and it is suitable for DFS.
            To mimic the recursive nature of DFS we use a stack to keep track of the frontier.     
    '''
    

    # create a set to keep track of explored states
    explored = set()

    # create a queue to keep track of the frontier 
    frontier = deque()

    # add the initial state to the frontier with an empty path
    frontier.append((initial_state , []))
    
    # loop until the frontier is empty
    while frontier :

        # pop the first state from the frontier
        state , path  = frontier.pop()

        # if the state is in the explored set continue
        if state in explored:
            continue
        
        # if the state is the goal state return the path
        if problem.is_goal(state):
            return path

        # add the state to the explored set
        explored.add(state)

        # loop over all the possible actions in the current state
        for action in problem.get_actions(state):

            # get the successors
            successor = problem.get_successor(state , action)

            # create a new path by appending the current action to the current path
            new_path = list(path)
            new_path.append(action)

            # add the successor to the frontier with the new path
            frontier.append((successor , new_path)) 

    # if the frontier is empty and the goal state is not found return None
    # this means that there is no solution
    return None

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()

    '''
        1.What the algorithm does :
            the algorithm uses a priority queue to keep track of the frontier
            The algorithm starts by adding the initial state to the frontier with the cost and the explored set.
            Then it loops until the frontier is empty.
            In each iteration the algorithm pops the state from the frontier which have the lowest cost and checks if it is the goal state.
            If it is the goal state it returns the path.
            If it is not the goal state the algorithm loops over all the possible actions in the current state.

        2.The data structure used : Priority Queue

        3.Why this data structure is used :
            To get the state with the lowest cost we use a priority queue.
    '''

    # create a set to keep track of explored states
    explored = set()

    # create a dictionary to keep track of the cost of each state
    cost = {initial_state : 0}

    # create a priority queue to keep track of the frontier 
    # the priority queue is a min heap and the priority is the cost of the state
    # the second element of the tuple is an index to make sure that the priority queue is stable    
    frontier = []
    heapq.heappush(frontier, (0 , 0 , initial_state , []))

    # create a counter to keep track of the index to make sure that the priority queue is stable
    index = 1

    while frontier:

        # pop the state with the lowest cost from the frontier
        path_cost , _ , state , path = heapq.heappop(frontier)

        # if the state is in the explored set continue
        if state in explored:
            continue

        # if the state is the goal state return the path
        if problem.is_goal(state):
            return path
            
        # add the state to the explored set
        explored.add(state)

        # loop over all the possible actions in the current state
        for action in problem.get_actions(state):

            # get the successors 
            successor = problem.get_successor(state, action)

            # check if the successor is not in the explored set
            if successor not in explored:

                # calculate the cost of the successor
                new_cost = path_cost + problem.get_cost(state, action)

                # if the successor have a lower cost than the current cost then continue
                if successor in cost and new_cost >= cost[successor]:
                    continue

                # create the new path by appending the current action to the current path
                new_path = list(path)
                new_path.append(action)

                # update the cost of the successor to the new cost in the cost dictionary
                cost[successor] = new_cost

                # add the successor to the frontier with the new path and the new cost
                heapq.heappush(frontier, (new_cost, index, successor,new_path))

                # increment the index
                index += 1
    
    # if the frontier is empty and the goal state is not found return None
    # this means that there is no solution
    return None
           
def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()

    '''
        1.What the algorithm does :
            the algorithm uses a priority queue to keep track of the frontier
            The algorithm starts by adding the initial state to the frontier with the cost and the explored set.
            Then it loops until the frontier is empty.
            In each iteration the algorithm pops the state from the frontier which have the lowest estimated cost and checks if it is the goal state.
            If it is the goal state it returns the path.
            If it is not the goal state the algorithm loops over all the possible actions in the current state.

        2.The data structure used : Priority Queue

        3.Why this data structure is used :
            To get the state with the lowest estimated cost we use a priority queue.    
    '''

    # create a set to keep track of explored states
    explored = set()
   
   # the estimated cost of the initial state is the heuristic value of the initial state
    estimated_cost = heuristic(problem,initial_state)

    # create a dictionary to keep track of the sum of actual cost and heuristic of each state
    estimated_cost_map = { initial_state : estimated_cost }

    # create a priority queue to keep track of the frontier
    # the priority queue is a min heap and the priority is the sum of actual cost and heuristic of the state
    # the second element of the tuple is an index to make sure that the priority queue is stable
    # the third element of the tuple is the actual cost of the state to use it later in the heuristic function of the successors
    # the fourth element of the tuple is the path to the current state
    # the fifth element of the tuple is the path
    frontier = []
    heapq.heappush(frontier, (estimated_cost , 0 ,0, initial_state , []))

    # create a counter to keep track of the index to make sure that the priority queue is stable
    index = 1

    # loop until the frontier is empty
    while frontier:

        # pop the state with the lowest cost from the frontier
        _ , _ , actual_cost , state , path = heapq.heappop(frontier)

        # if the state is in the explored set continue
        if state in explored:
            continue

        # if the state is the goal state return the path
        if problem.is_goal(state):
            return path

        # add the state to the explored set
        explored.add(state)

        # loop over all the possible actions in the current state
        for action in problem.get_actions(state):

            # get the successors
            successor = problem.get_successor(state, action)

            # check if the successor is not in the explored set
            if successor not in explored:

                # calculate the actual cost of the successor
                new_cost = actual_cost + problem.get_cost(state, action) 

                # calculate the estimated cost of the successor
                new_heuristic = heuristic(problem,successor) + new_cost

                # if the successor have a lower cost than the current cost then continue
                if successor in estimated_cost_map and new_heuristic >= estimated_cost_map[successor]:
                    continue

                # create the new path by appending the current action to the current path
                new_path = list(path)
                new_path.append(action)

                # update the estimated cost of the successor to the new estimated cost in the estimated_cost_map dictionary
                estimated_cost_map[successor] = new_heuristic

                # add the successor to the frontier with the new path and the new estimated cost
                heapq.heappush(frontier, (new_heuristic, index,new_cost,  successor, new_path))

                # increment the index
                index += 1

    # if the frontier is empty and the goal state is not found return None
    return None

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()

    '''
        1.What the algorithm does :
            the algorithm uses a priority queue to keep track of the frontier
            The algorithm starts by adding the initial state to the frontier with the cost and the explored set.
            Then it loops until the frontier is empty.
            In each iteration the algorithm pops the state from the frontier which have the lowest heuristic cost and checks if it is the goal state.
            If it is the goal state it returns the path.
            If it is not the goal state the algorithm loops over all the possible actions in the current state.

        2.The data structure used : Priority Queue

        3.Why this data structure is used :
            To get the state with the lowest heuristic cost we use a priority queue.
    '''

    # create a set to keep track of explored states
    explored = set()

    # the estimated cost of the initial state is the heuristic value of the initial state
    heuristic_cost = heuristic(problem,initial_state)

    # create a dictionary to keep track of the heuristic cost of each state
    heuristic_cost_map = { initial_state : heuristic_cost }

    # create a priority queue to keep track of the frontier
    # the priority queue is a min heap and the priority is the heuristic cost of the state
    # the second element of the tuple is an index to make sure that the priority queue is stable
    # the third element of the tuple is the state
    # the fourth element of the tuple is the path
    frontier = []
    heapq.heappush(frontier, (heuristic_cost , 0 , initial_state, []))

    # create a counter to keep track of the index to make sure that the priority queue is stable
    index = 1

    # loop until the frontier is empty
    while frontier:

        # pop the state with the lowest cost from the frontier (the state with the lowest heuristic cost)
        _ , _ , state , path = heapq.heappop(frontier)

        # if the state is in the explored set continue
        if state in explored:
            continue

        # if the state is the goal state return the path
        if problem.is_goal(state):
            return path

        # add the state to the explored set
        explored.add(state)

        # loop over all the possible actions in the current state
        for action in problem.get_actions(state):

            # get the successors
            successor = problem.get_successor(state, action)

            # check if the successor is not in the explored set
            if successor not in explored:

                # calculate the heuristic cost of the successor
                new_heuristic = heuristic(problem,successor) 

                # if the successor have a lower cost than the current cost then continue
                if successor in heuristic_cost_map and new_heuristic >= heuristic_cost_map[successor]:
                    continue

                # create the new path by appending the current action to the current path
                new_path = list(path)
                new_path.append(action)

                # update the heuristic cost of the successor to the new heuristic cost in the heuristic_cost_map dictionary
                heuristic_cost_map[successor] = new_heuristic

                # add the successor to the frontier with the new path and the new heuristic cost
                heapq.heappush(frontier, (new_heuristic, index,  successor , new_path))

                # increment the index
                index += 1

    # if the frontier is empty and the goal state is not found return None
    return None