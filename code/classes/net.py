from wire import Wire
from gate import Gate


class Net():
    
    def __init__(self, gate_a: Gate, gate_b: Gate):
        """
        PRE: The chip_id's of the two chips to be connected
        POST: Initializes a net object"""
                
        self.gates = (gate_a, gate_b)
        self.wiring: list[Wire] = []


    def add_wire(self, wire: Wire) -> None:
        """
        PRE: The x and y coordinates for a wire
        POST: Wire has been added to front of self.wiring"""

        self.wiring.append(wire)


    def unadd_wire(self) -> None:
        """
        POST: Last wire has been removed from self.wiring"""
        self.wiring.pop()


    def get_wire_positions(self) -> list[set[int]]:
        """
        POST: Returns list of coördinate sets for all the wires in self.wiring"""
                
        return [(wire.x, wire.y) for wire in self.wiring]


    def __repr__(self) -> str:
        """
        POST: string representation of net"""
        
        return f"{self.gates[0]} | {self.gates[1]}"
