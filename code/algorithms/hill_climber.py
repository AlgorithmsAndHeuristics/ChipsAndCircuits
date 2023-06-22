from circuit import Circuit
from collections import defaultdict
from wire import Wire


class HillClimber():
    
    def __init__(self, circuit: Circuit) -> None:
        self.circuit: Circuit = circuit
        
        # Assuming that the circuit initially has no collisions, get the gate coordinates to exclude from later collision checking
        self.gate_coordinates: list[tuple[int, int, int]] = []
        self.gate_coordinates = self.get_colliding_coordinates()
        
        self.shorten_longest_wire()
        print(self.get_colliding_coordinates())
    
    
    def get_colliding_coordinates(self) -> list[tuple[int, int, int]]:
        print('get_colliding_coordinates()')
        
        # NOTE: Tracking wire objects will not work because they are never identical in Python even though their coordinates are
        coordinates: list[tuple[int, int, int]] = []
        colliding_coordinates: list[tuple[int, int, int]] = []
        
        for netlist in self.circuit.netlists:
            for net in netlist.nets.values():
                for wire in net.wiring:
                    coordinate: tuple[int, int, int] = (wire.x, wire.y, wire.z)
                    
                    # Check if coordinate of wire collides with another wire
                    if coordinate in coordinates:
                        colliding_coordinates.append(coordinate)
                    
                    coordinates.append(coordinate)
        
        # Remove gate coordinates from colliding coordinates
        return [coordinate for coordinate in colliding_coordinates if coordinate not in self.gate_coordinates]
    
    
    def shorten_longest_wire(self) -> None:
        for netlist in self.circuit.netlists:
            # Sort nets by wire length from longest to shortest
            nets = sorted(netlist.nets.values(), key=lambda net: len(net.wiring), reverse=True)
            
            for net in nets:
                # Get first wire to match gates
                first_wire = net.wiring[0]
                
                wiring_z = defaultdict(list)
                
                for wire in net.wiring:
                    # Set Z-coordinate to match first wire
                    wire.z = first_wire.z
                    
                    # Group wiring by Z-coordinate
                    wiring_z[wire.z].append(wire)
                
                # Shorten wiring by retaining the largest wiring group
                net.wiring = wiring_z[max(wiring_z, key=lambda wire: wire)]
                
                # Temporary: Stop after the first wire
                break
