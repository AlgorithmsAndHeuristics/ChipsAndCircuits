import pandas as pd

class Net():
    
    def __init__(self, chip_a: int, chip_b: int):
        """
        PRE: the chip_id's of the two chips to be connected
        POST: Initializes a net object"""
                
        self.gates = [chip_a, chip_b]
        self.wiring = []


    def add_wire(self, x: int, y: int):
        """
        PRE: the x and y coördinates for a wire
        POST: Wire has been added do self.wiring"""

        self.wiring.append((x, y))


class Netlist():
    
    def __init__(self, netlist_path: str):
        """
        PRE: a path to a netlist_x.csv
        POST: Initializes a Netlist object"""

        # load the data from the csv
        df = pd.read_csv(netlist_path)
        self.nets = [(net['chip_a'], net['chip_b']) for idx, net in df.iterrows()]
        
        
    def get_wire_count(self) -> int:
        """
        POST: Returns the current total amount of wires
        in net.wiring for all the nets in the netlist"""

        return sum(len(net.wiring for net in self.nets))
    

    def get_intersections(self) -> list[Net, set[int]]:
        """
        POST: Return a list of intersecting nets and
        the coördinates of the intersection"""

        intersections = []

        # Compare each net in the netlist
        for net1 in self.nets:
            for net2 in self.nets[1:]:

                # check if the two nets share a wire position
                if bool(set(net1.wiring) & set(net2.wiring)):
                    intersections.append(net1, net2, net1.wiring)

        return intersections

    
    def get_cost(self) -> int:
        """
        POST: Return the cost of the netlist"""

        return self.get_wire_count() + 300 * len(self.get_intersections)