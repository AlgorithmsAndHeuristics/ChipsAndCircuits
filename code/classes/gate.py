import math

class Gate():

    def __init__(self, id: int, position: tuple[int, int]) -> None:
        """
        PRE: Id of type integer, position of type tuple[int, int]
        POST: Initializes a Gate object"""


        self.id = id
        self.position = position

    
    def get_distance(self, other_gate: 'Gate') -> int:
        """
        Gets the distance between two gates.
        PRE: other_gate of type Gate
        POST: distance between the gates rounded up as int"""


        dx = abs(self.position[0] - other_gate.position[0])
        dy = abs(self.position[1] - other_gate.position[1])
        return int(math.sqrt(dx**2 * dy**2))
