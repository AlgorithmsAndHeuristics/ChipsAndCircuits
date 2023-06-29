import math

class Gate():

    def __init__(self, id: int, position: tuple[int, int]) -> None:
        """
        PRE: Id of type integer, position of type tuple[int, int]
        POST: Initializes a Gate object"""

        self.id = id
        self.position = position
        # NOTE fix position z axis
        # either in function var or
        # self.position = (position[0], position[1], 0)

    
    def __repr__(self) -> str:
        return f"{self.id}: {self.position}"
    
    
    def get_distance(self, other_gate: 'Gate') -> int:
        """
        Gets the distance between two gates.
        PRE: Other_gate of type Gate
        POST: Distance between the gates rounded up as int"""

        dx = abs(self.position[0] - other_gate.position[0])
        dy = abs(self.position[1] - other_gate.position[1])

        return int(math.sqrt(dx**2 * dy**2))


    def __getstate__(self):
        """
        Return a dictionary of the Gate's state."""
        
        return {'id': self.id, 'position': self.position}


    def __setstate__(self, state):
        """
        Restore the Gate's state from the state dictionary."""

        self.id = state['id']
        self.position = state['position']
