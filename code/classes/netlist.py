from intersection import Intersection
from net import Net
import pandas as pd


class Netlist():
    
    def __init__(self, netlist_path: str):
        """
        PRE: A path to a netlist_x.csv
        POST: Initializes a Netlist object"""

        # Load the data from the csv
        df = pd.read_csv(netlist_path)
        self.nets = [Net(net['chip_a'], net['chip_b']) for _, net in df.iterrows()]
    
    
    def check_intersection(self, net1: Net, net2: Net) -> bool:
        """
        Check if a connection between two Nets has an intersection"""
        for intersection in self.get_intersections():
            if (intersection.net1 == intersected_net1 and intersection.net2 == intersected_net2) or \
                (intersection.net2 == intersected_net1 and intersection.net1 == intersected_net2):
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

        # Compare each net in the netlist
        for i in range(len(self.nets)):
            net1 = self.nets[i]
            
            for j in range(i + 1, len(self.nets)):
                net2 = self.nets[j]

                # Check if the two nets share a wire position
                if bool(set(net1.wiring) & set(net2.wiring)):
                    intersections.add(Intersection(net1, net2, net1.wiring))

        return intersections
    
    
    def get_wire_count(self) -> int:
        """
        POST: Returns the current total amount of wires
        in net.wiring for all the nets in the netlist"""

        return sum(len(net.wiring) for net in self.nets)


    def __repr__(self) -> str:
        """
        POST: Returns string represenatation of netlist"""
        
        string = "chip_a | chip_b\n"
        for net in self.nets:
            string += f"{net.gates[0]}".rjust(6, " ") + " | " + f"{net.gates[1]}".rjust(6, " ") + "\n"

        return string
