from .net import Net
from .wire import Wire


class Intersection():
    
    def __init__(self, net1: Net, net2: Net, wiring: list[Wire]):
        self.net1 = net1
        self.net2 = net2
        self.wiring = wiring
