class Wire():

    def __eq__(self, other: any): 
        if not isinstance(other, Wire):
            # Do not attempt to compare against unrelated types
            return NotImplemented

        return self.x == other.x and self.y == other.y and self.z == other.z


    def __init__(self, x: int, y: int, z: int = 0):
        """
        PRE: x, y and z coördinates.
        POST: initializes a Wire object.
        """

        self.x = x
        self.y = y
        self.z = z
    
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"


    def __getstate__(self):
        """
        Return a dictionary of the Wire's state."""
        
        return {'x': self.x, 'y': self.y, 'z': self.z}


    def __setstate__(self, state):
        """
        Restore the Wire's state from the state dictionary."""

        self.x = state['x']
        self.y = state['y']
        self.z = state['z']
