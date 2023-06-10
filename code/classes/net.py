class Net():
    
    def __init__(self, chip_a: int, chip_b: int):
        """
        PRE: The chip_id's of the two chips to be connected
        POST: Initializes a net object"""
                
        self.gates = (chip_a, chip_b)
        self.wiring: list[tuple[int, int]] = []


    def add_wire(self, x: int, y: int):
        """
        PRE: The x and y coördinates for a wire
        POST: Wire has been added do self.wiring"""

        self.wiring.append((x, y))
