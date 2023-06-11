from .wire import Wire


class Net():
    
    def __init__(self, chip_a: int, chip_b: int):
        """
        PRE: The chip_id's of the two chips to be connected
        POST: Initializes a net object"""
                
        self.gates = (chip_a, chip_b)
        self.wiring: list[Wire] = []


    def add_wire(self, x: int, y: int):
        """
        PRE: The x and y coordinates for a wire
        POST: Wire has been added do self.wiring"""

        self.wiring.append(Wire(x, y))

    def __repr__(self) -> str:
        """
        POST: string representation of net"""
        string = f"{self.gates[0]}".rjust(6, " ") + " | " + f"{self.gates[1]}".rjust(6, " ") 
        
        return 