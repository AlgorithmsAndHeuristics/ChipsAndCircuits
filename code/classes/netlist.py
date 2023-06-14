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
                position = [pos for pos in net1.get_wire_positions() if pos in net2.get_wire_positions()]

                if bool(position):
                    intersections.add(Intersection(net1, net2, position[0][0], position[0][1]))

        return intersections
    
    
    def get_wire_count(self) -> int:
        """
        POST: Returns the current total amount of wires
        in net.wiring for all the nets in the netlist"""

        return sum(len(net.wiring) for _, net in self.nets2)
