from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json

from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #TODO: Complete this function
        # NotImplemented()

        # if the state is terminal , return 0
        if self.mdp.is_terminal(state):
            return 0
        
        # as the the reward is a function of current state, action and next state , we need to use the following variant of bellman equation
        # U(s) = max( sum( P(s'|s,a) * (R(s,a,s') + gamma * U(s')) for s' in S ) for a in A )
        # where S is the set of all possible states and A is the set of all possible actions        
        # self.mdp.get_successor(state, action)[next_state] gives the probability of next_state given state and action
        utility = max(sum( self.mdp.get_successor(state, action)[next_state] * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state]) for next_state in self.mdp.get_successor(state, action) ) for action in self.mdp.get_actions(state) )

        # return the utility computed using the bellman equation
        return utility  
    
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        #TODO: Complete this function
        # NotImplemented()

        # create temp to store the updated utilities to update the utilities after computing all the utilities
        # this is done to avoid updating the utilities before all the utilities are computed
        # this is because the utilities are used in the computation of other utilities            
        utility_updates = {}

        # loop over all the states in the MDP 
        for state in self.mdp.get_states():

            # store the updated utility in the utility_updates dictionary
            utility_updates[state] = self.compute_bellman(state)

        # compute the maximum change in the utilities
        max_change = max(abs(utility_updates[state] - self.utilities[state]) for state in self.mdp.get_states())

        for state in self.mdp.get_states():

            # update the utilities
            self.utilities[state] = utility_updates[state]

        # return True if the maximum change in the utilities is less than or equal to the tolerance
        # return False otherwise
        return max_change <= tolerance

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        iteration = 0
        while iterations is None or iteration < iterations:
            iteration += 1
            if self.update(tolerance):
                break
        return iteration
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function
        # NotImplemented()

        # if the state is terminal , return None
        if self.mdp.is_terminal(state):
            return None   

        # get the action that have the maximum expected utility
        # this is the same code as in the bellman equation, but instead of computing the maximum utility, we compute the action that has the maximum utility
        # if there are more than one action that have the maximum utility, return the first action that appears in the "actions" list        
        action = max(self.mdp.get_actions(state), key = lambda action: sum( self.mdp.get_successor(state, action)[next_state] * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state]) for next_state in self.mdp.get_successor(state, action) ))

        # return the action that has the maximum expected utility
        return action
    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
