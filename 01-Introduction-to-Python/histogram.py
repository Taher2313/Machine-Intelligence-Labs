from typing import Any, Dict, List
import utils


def histogram(values: List[Any]) -> Dict[Any, int]:
    '''
    This function takes a list of values and returns a dictionary that contains the list elements alongside their frequency
    For example, if the values are [3,5,3] then the result should be {3:2, 5:1} since 3 appears twice while 5 appears once 
    '''
    # TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()

    # check if values is empty
    if len(values) == 0:
        return {}

    # create a dictionary to store the frequency of each value
    frequency_dict = {}
    for i in values:
        if i in frequency_dict:
            frequency_dict[i] += 1
        else:
            frequency_dict[i] = 1

    return frequency_dict
