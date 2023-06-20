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