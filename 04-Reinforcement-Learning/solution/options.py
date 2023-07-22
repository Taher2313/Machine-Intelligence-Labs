# This file contains the options that you should modify to solve Question 2

def question2_1():
    #TODO: Choose options that would lead to the desired results 
    # here to make the agent prefer the dangerous path over the safe path and 
    # take the first small exit reward over the second large exit reward, 
    # we will make the living big negtive reward
    # and will let the environment to be stochastic with noise 0.2
    # to 
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -3
    }

def question2_2():
    #TODO: Choose options that would lead to the desired results
    # to make the agent prefer the safe path over the dangerous path ,
    # we will make the living reward small negative number
    # and to make him choose the first small exit reward over the second large exit reward,
    # we will decrease the discount factor
    return {
        "noise": 0.2,
        "discount_factor": 0.2,
        "living_reward": -0.04
    }

def question2_3():
    #TODO: Choose options that would lead to the desired results
    # here to make the agent prefer the dangerous path over the safe path and 
    # take the second large exit reward over the first small exit reward,
    # we will make the living big negtive reward
    # but it is bigger than what we choose in question2_1
    # so the living reward will not harm him alot and 
    # make the agent prefer the second large exit reward over the first small exit reward
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -2
    }

def question2_4():
    #TODO: Choose options that would lead to the desired results
    # here to make the agent prefer the safe path over the dangerous path ,
    # we will make the living reward small negative number
    # and to make him choose the second large exit reward over the first small exit reward,
    # we will leave the discount factor as it is 1 
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -0.1
    }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    # to make the policy avoid any terminal state and keep the episode going on forever.
    # we will make the living reward positive number in a deterministic environment
    return {
        "noise": 0.0,
        "discount_factor": 1.0,
        "living_reward": 0.1
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    # to make the agent seek the exit as fast as possible,
    # we will make the living reward large negative number  
    # and keep the environment deterministic with noise 0
    # also the environment could be stochastic with noise 0.2
    return {
        "noise": 0.0,
        "discount_factor": 1.0,
        "living_reward": -20
    }