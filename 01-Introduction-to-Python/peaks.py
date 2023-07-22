from typing import List
import utils


def peaks(seq: List[int]) -> int:
    '''
    This function takes sequence of integers and returns the number of peaks.
    A peak is an element in the sequence whose value is higher than the two elements surrounding it.
    The first and last elements cannot be peaks.
    Any list containing less than 3 elements will have 0 peaks. 
    '''
    # TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()

    # check if sequence is empty or has less than 3 elements
    if len(seq) < 3:
        return 0

    num_peaks = 0
    for i in range(1, len(seq) - 1):
        if seq[i-1] < seq[i] > seq[i+1]:
            num_peaks += 1

    return num_peaks
