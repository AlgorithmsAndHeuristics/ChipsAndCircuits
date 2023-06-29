from net import Net

class Intersection():
    
    def __init__(self, net1: Net, net2: Net, x: int, y: int, z: int):
        self.net1 = net1
        self.net2 = net2
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"{self.net1} & {self.net2}: at ({self.x}, {self.y}, {self.z})"
    

    def __getstate__(self):
        """
        Return a dictionary of the Intersection's state."""
        
        return {'net1': self.net1, 'net2': self.net2, 'x': self.x, 'y': self.y, 'z': self.z}


    def __setstate__(self, state):
        """
        Restore the Intersection's state from the state dictionary."""

        self.net1 = state['net1']
        self.net2 = state['net2']
        self.x = state['x']
        self.y = state['y']
        self.z = state['z']
