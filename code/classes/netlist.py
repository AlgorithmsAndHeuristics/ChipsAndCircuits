from intersection import Intersection
from net import Net
from gate import Gate
import pandas as pd


class Netlist():
    
    def __init__(self, netlist_path: str, gates: dict[int, Gate]):
        """
        PRE: A path to a netlist_x.csv
        POST: Initializes a Netlist object"""

        # Load the data from the csv
        df = pd.read_csv(netlist_path)
        self.nets: list[Net] = [Net(gates[net['chip_a']], gates[net['chip_b']]) for _, net in df.iterrows()]
        self.nets2: dict[int, Net] = { i: Net(gates[net['chip_a']], gates[net['chip_b']]) for i, net in df.iterrows() }
    
    
    def check_intersection(self, net1: Net, net2: Net) -> bool:
        """
        Check if a connection between two Nets has an intersection"""
        
        for intersection in self.get_intersections():
            if (intersection.net1 == net1 and intersection.net2 == net2) or \
                (intersection.net2 == net1 and intersection.net1 == net2):
                return True
        
        return False
    
    
    def direct_distances(self) -> int:
        """
        Get all the direct distances of the nets.

        POST: returns a list of tuples of type tuple[int, int]:
        (net_id, distance)
        """

        distance_list = []
        for net_id in self.nets2:
            net = self.nets2[net_id]
            distance = net.direct_distance()
            distance_list.append((net_id, distance))

        return distance_list


    def get_cost(self) -> int:
        """
        POST: Return the cost of the netlist, according to the formula: C = n + 300 * k"""

        return self.get_wire_count() + 300 * len(self.get_intersections())
    
    
    def get_intersections(self) -> set[Intersection]:
        """
        POST: Return a set of intersecting nets and
        the coordinates of the intersection"""

        intersections = set()
        len_nets: int = len(self.nets2)

        # Compare each net in the netlist
        for i in range(len_nets):
            net1: Net = self.nets2[i]
            
            for j in range(i + 1, len_nets):
                net2: Net = self.nets2[j]

                # Check if the two Nets share a wire position
                positions = [pos for pos in net1.get_wire_positions() if pos in net2.get_wire_positions()]

                if bool(positions):
                    #TODO FIX THIS IN gate.py
                    net1_gate1_position = net1.gates[0].position
                    net1_gate1_position = (net1_gate1_position[0], net1_gate1_position[1], 0)
                    net1_gate2_position = net1.gates[1].position
                    net1_gate2_position = (net1_gate2_position[0], net1_gate2_position[1], 0)
                    net2_gate1_position= net2.gates[0].position
                    net2_gate1_position = (net2_gate1_position[0], net2_gate1_position[1], 0)
                    net2_gate2_position = net2.gates[1].position
                    net2_gate2_position = (net2_gate2_position[0], net2_gate2_position[1], 0)
                    # Don't add intersections on gates
                    for position in positions:
                        if position != net1_gate1_position and position != net1_gate2_position and\
                            position != net2_gate1_position and position != net2_gate2_position:
                            intersections.add(Intersection(net1, net2, position[0], position[1], position[2]))

        return intersections
    
    
    def get_wire_count(self) -> int:
        """
        POST: Returns the current total amount of wires
        in net.wiring for all the nets in the netlist"""

        return sum(len(net.wiring) for net in self.nets2.values())
