from wire import Wire
from gate import Gate


class Net():
    
    def __init__(self, gate_a: Gate, gate_b: Gate):
        """
        PRE: The chip_id's of the two chips to be connected
        POST: Initializes a net object"""
                
        self.gates = (gate_a, gate_b)
        self.wiring: list[Wire] = []


    def __repr__(self) -> str:
        """
        POST: string representation of net"""
        
        return f"{self.gates[0]} | {self.gates[1]}"


    def add_wire(self, wire: Wire) -> None:
        """
        PRE: The x and y coordinates for a wire
        POST: Wire has been added to front of self.wiring"""

        self.wiring.append(wire)


    def clear_wiring(self) -> None:
        self.wiring = []
    
    
    def direct_distance(self) -> int:
        """
        Get the direct distance between the gates.

        POST: distance of type int
        """

        gate_1, gate_2 = self.gates[0], self.gates[1]
        return sum(tuple(abs(i - j) for i, j in zip(gate_1.position, gate_2.position)))
        

    def lay_wiring(self) -> None:
        pass


    def get_wire_positions(self) -> list[set[int]]:
        """
        POST: Returns list of coördinate sets for all the wires in self.wiring"""
                
        return [(wire.x, wire.y, wire.z) for wire in self.wiring]


    def unadd_wire(self) -> None:
        """
        POST: Last wire has been removed from self.wiring"""
        self.wiring.pop()

