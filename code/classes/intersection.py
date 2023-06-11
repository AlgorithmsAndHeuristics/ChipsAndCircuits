from net import Net
from wire import Wire

class Intersection():
    
    def __init__(self, net1: Net, net2: Net, x: int, y: int):
        self.net1 = net1
        self.net2 = net2
        self.x = x
        self.y = y
