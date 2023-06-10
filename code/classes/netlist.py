from net import Net
import pandas as pd


class Netlist():
    
    def __init__(self, netlist_path: str):
        """
        PRE: A path to a netlist_x.csv
        POST: Initializes a Netlist object"""

        # load the data from the csv
        df = pd.read_csv(netlist_path)
        self.nets = [Net(net['chip_a'], net['chip_b']) for idx, net in df.iterrows()]
    
    
    def check_intersection(self) -> None:
        pass
    
    
    def get_cost(self) -> int:
        """
        POST: Return the cost of the netlist, according to the formula: C = n + 300 * k"""

        return self.get_wire_count() + 300 * len(self.get_intersections())
    
    
    def get_intersections(self) -> list[tuple[Net, Net, list[tuple[int, int]]]]:
        """
        POST: Return a list of intersecting nets and
        the coördinates of the intersection"""

        intersections = []

        # Compare each net in the netlist
        for i in range(len(self.nets)):
            net1 = self.nets[i]
            
            for j in range(i+1, len(self.nets)):
                net2 = self.nets[j]

                # Check if the two nets share a wire position
                if bool(set(net1.wiring) & set(net2.wiring)):
                    intersections.append((net1, net2, net1.wiring))

        return intersections
    
    
    def get_wire_count(self) -> int:
        """
        POST: Returns the current total amount of wires
        in net.wiring for all the nets in the netlist"""

        return sum(len(net.wiring) for net in self.nets)
    
    
    # TODO: Decide whether to create this method to use in __init__ or not
    #def load_csv(self) -> None:
    #    df: pd.DataFrame = pd.read_csv('print_0.csv')
    #    
    #    # Since each row represents a Net, add them to self.nets
    #    for row in df.rows:
    #        net: Net = Net(row['chip'], row['chip']) # TODO: Differentiate between chip_a and chip_b when initializing
    #        net.add_wire(row['x'], row['y'])
    #        self.nets.append(net)
