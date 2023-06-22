from circuit import Circuit
from collections import defaultdict
from manhattan_path import make_manhattan_connection
from net import Net
from netlist import Netlist
from wire import Wire


class HillClimber():
    
    def __init__(self, circuit: Circuit) -> None:
        netlist_id: int = 0
        
        self.circuit: Circuit = circuit
        self.netlist: Netlist = circuit.netlists[netlist_id]
        
        # Track rewired nets to prevent re-rewiring
        self.rewired_nets: list[Net] = []
        
        # Assuming that the circuit initially has no collisions, get the gate coordinates to exclude from later collision checking
        self.gate_coordinates: list[tuple[int, int, int]] = []
        self.gate_coordinates = self.get_colliding_coordinates()
        
        self.shorten_longest_wire()
        
        for net in self.get_nets_with_colliding_coordinates():
            # Clear wiring of nets with colliding coordinates
            net.clear_wiring()
            
            # Re-create wiring of nets with previously colliding coordinates
            #make_manhattan_connection(net)
            net_id: int = list(self.netlist.nets.keys())[list(self.netlist.nets.values()).index(net)]
            circuit.lay_shortest_line(netlist_id, net_id)
    
    
    def get_colliding_coordinates(self) -> list[tuple[int, int, int]]:
        # NOTE: Wire.__eq__ is not used here because gate coordinates must be considered as well
        coordinates: list[tuple[int, int, int]] = []
        colliding_coordinates: list[tuple[int, int, int]] = []
        
        for net in self.netlist:
            for wire in net.wiring:
                coordinate: tuple[int, int, int] = (wire.x, wire.y, wire.z)
                
                # Check if coordinate of wire collides with another wire
                if coordinate in coordinates:
                    colliding_coordinates.append(coordinate)
                
                coordinates.append(coordinate)
        
        # Remove gate coordinates from colliding coordinates
        return [coordinate for coordinate in colliding_coordinates if coordinate not in self.gate_coordinates]
    
    
    def get_nets_with_colliding_coordinates(self) -> set[Net]:
        nets: set[Net] = set()
        
        for net in self.netlist:
            for wire in net.wiring:
                coordinate: tuple[int, int, int] = (wire.x, wire.y, wire.z)
                
                for colliding_coordinate in self.get_colliding_coordinates():
                    # Check if a wire's coordinate is one of the known colliding coordinates
                    if coordinate == colliding_coordinate:
                        nets.add(net)
                        break
        
        # Remove rewired nets from nets with colliding coordinates
        return [net for net in nets if net not in self.rewired_nets]
    
    
    def shorten_longest_wire(self) -> None:
        # Sort nets by wire length from longest to shortest
        nets = sorted(self.netlist, key=lambda net: len(net.wiring), reverse=True)
        
        for net in nets:
            # Get first wire to match gates in new wiring later
            first_wire = net.wiring[0]
            
            wiring_z = defaultdict(list)
            
            for wire in net.wiring:
                # Set Z-coordinate to match first wire
                wire.z = first_wire.z
                
                # Group wiring by Z-coordinate
                wiring_z[wire.z].append(wire)
            
            # Shorten wiring by retaining the largest wiring group
            net.wiring = wiring_z[max(wiring_z, key=lambda wire: wire)]
            
            self.rewired_nets.append(net)
            
            # Temporary: Stop after the first wire
            break
