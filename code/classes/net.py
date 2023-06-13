from wire import Wire


class Net():
    
    def __init__(self, chip_a: int, chip_b: int):
        """
        PRE: The chip_id's of the two chips to be connected
        POST: Initializes a net object"""
                
        self.gates = (chip_a, chip_b)
        self.wiring: list[Wire] = []


    def __repr__(self) -> str:
        """
        POST: string representation of net"""
        
        return f"chip_a | chip_b\n{self.gates[0]:>6} | {self.gates[1]:>6}"


    def add_wire(self, x: int, y: int):
        """
        PRE: The x and y coordinates for a wire
        POST: Wire has been added do self.wiring"""

        self.wiring.append(Wire(x, y))


    def get_wire_positions(self) -> list[set[int]]:
        return [(wire.x, wire.y) for wire in self.wiring]
