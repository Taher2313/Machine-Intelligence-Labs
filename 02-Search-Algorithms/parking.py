from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers import utils

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point]
# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        # utils.NotImplemented()

        # return the initial state of the of the cars (the cars tuple)
        return self.cars
         
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        #TODO: ADD YOUR CODE HERE
        # utils.NotImplemented()
        
        # check if that all the cars are in their parking slots 
        # if yes then return True else return False        
        for i in range(len(state)):
            if state[i] not in self.slots or self.slots[state[i]] != i:
                return False
        return True

    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        #TODO: ADD YOUR CODE HERE
        # utils.NotImplemented()

        actions = []

        # check for every car if it can move in any direction
        # the location is valid if it is in the passages (not a wall) 
        # and it is not in the state (not another car's location)
        # if it is valid then add it to the actions list

        for i in range(len(state)):
            for direction in Direction:
                new_location = state[i] + direction.to_vector()
                if new_location in self.passages and new_location not in state:
                    actions.append((i, direction))
        return actions

                 
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        # utils.NotImplemented()

        # get the car number and the direction
        car_num = action[0]
        direction = action[1].to_vector()

        # get the car current position of the car
        car_position = state[car_num]

        # get the new location of the car after moving by adding the direction to the current position
        new_location = car_position + direction

        # create a new state list and update the location of the car in the new state
        new_state = list(state)
        new_state[car_num] = new_location

        # cast the new state list to tuple and return it
        return tuple(new_state)


    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        #TODO: ADD YOUR CODE HERE
        # utils.NotImplemented()

        # get the car number and the direction
        car_num = action[0]
        direction = action[1].to_vector()

        # get the car current position of the car
        car_position = state[car_num]

        # get the new location of the car after moving by adding the direction to the current position
        new_location = car_position + direction

        # check weather the new location is the goal location or it not in the parking slots (not a parking slot for other car)
        if new_location not in self.slots or self.slots[new_location] == car_num:
            return 1
        else:
            return 101
    
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
