from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
import numpy as np

from helpers.utils import NotImplemented

# This is a class for a generic Policy Iteration agent
class PolicyIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training
    policy: Dict[S, A]
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        # This initial policy will contain the first available action for each state,
        # except for terminal states where the policy should return None.
        self.policy = {
            state: (None if self.mdp.is_terminal(state) else self.mdp.get_actions(state)[0])
            for state in self.mdp.get_states()
        }
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given the utilities for the current policy, compute the new policy
    def update_policy(self):
        #TODO: Complete this function
        # NotImplemented()

        # loop through all states to update the policy
        for state in self.mdp.get_states():

            # if the state is terminal, then the policy is None
            if self.mdp.is_terminal(state):
                self.policy[state] = None
            else:

                # find the action that maximizes the utility
                # initialize the max_action and max_value
                max_action = None
                max_value = float('-inf')

                # loop through all actions in the current state to find the action that maximizes the utility
                for action in self.mdp.get_actions(state):

                    # compute the utility for the current action
                    # initialize the utility to be 0 
                    value = 0

                    # loop through all possible next states due to the current action
                    for next_state, prob in self.mdp.get_successor(state, action).items():

                        # compute the reward for the current action and next state
                        reward = self.mdp.get_reward(state, action, next_state)

                        # compute the utility for the current action and next state
                        value += prob * (reward + self.discount_factor * self.utilities[next_state])

                    # if the utility for the current action is greater than the max_value, then update the max_value and max_action    
                    if value > max_value:
                        max_value = value
                        max_action = action

                # update the policy for the current state with the max_action
                self.policy[state] = max_action

                    
    
    # Given the current policy, compute the utilities for this policy
    # Hint: you can use numpy to solve the linear equations. We recommend that you use numpy.linalg.lstsq
    def update_utilities(self):
        #TODO: Complete this function
        # NotImplemented()

        # get the list of states in the MDP
        states = self.mdp.get_states()

        # let n be the number of states in the MDP
        n = len(states)

        # initialize the matrix A and vector b
        # A is an n x n matrix
        # b is an n x 1 vector
        # A and b are used to solve the linear equations
        # the linear equations are of the form A * x = b
        # A is the matrix of coefficients
        # x is the vector of unknowns (the utilities)
        # b is the vector of constants 
        A = np.zeros((n, n))
        b = np.zeros(n)

        # loop through all states to update the matrix A and vector b
        for i, state in enumerate(states):

            # check if the state is terminal
            if self.mdp.is_terminal(state):
                A[i, i] = 1
                b[i] = 0
            else:

                # get the action for the current state from the policy
                action = self.policy[state]

                # initialize the diagonal element of the matrix A to be 1
                A[i, i] = 1

                # loop through all possible next states due to the current action
                for j, next_state in enumerate(states):

                    # get the probability of the next state due to the current action
                    prob = self.mdp.get_successor(state, action).get(next_state, 0)

                    # get the reward for the current action and next state
                    reward = self.mdp.get_reward(state, action, next_state)

                    # update the matrix A and vector b
                    A[i, j] -= self.discount_factor * prob
                    b[i] += prob * reward

        # solve the linear equations to get the utilities
        x = np.linalg.lstsq(A, b, rcond=None)[0]

        # update the utilities
        for i, state in enumerate(states):
            self.utilities[state] = x[i]

    
    # Applies a single utility update followed by a single policy update
    # then returns True if the policy has converged and False otherwise
    def update(self) -> bool:
        #TODO: Complete this function
        # NotImplemented()

        # update the utilities
        self.update_utilities()

        # store the current policy to compare with the new policy
        current_policy = self.policy.copy()

        # update the policy
        self.update_policy()

        # return True if the policy has converged and False otherwise
        return current_policy == self.policy


    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None) -> int:
        iteration = 0
        while iterations is None or iteration < iterations:
            iteration += 1
            if self.update():
                break
        return iteration
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function
        # NotImplemented()

        # return None if the state is terminal
        if self.mdp.is_terminal(state):
            return None

        # return the best action which learned from the utilities and the MDP
        # whic is represented by the policy
        return self.policy[state]

    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            policy = {
                self.mdp.format_state(state): (None if action is None else self.mdp.format_action(action)) 
                for state, action in self.policy.items()
            }
            json.dump({
                "utilities": utilities,
                "policy": policy
            }, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            data = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in data['utilities'].items()}
            self.policy = {
                self.mdp.parse_state(state): (None if action is None else self.mdp.parse_action(action)) 
                for state, action in data['policy'].items()
            }
