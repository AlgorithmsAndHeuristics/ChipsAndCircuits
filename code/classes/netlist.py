import pandas as pd

class Net():
    
    def __init__(self, chip_a, chip_b):
        self.gates = [chip_a, chip_b]
        self.wiring = []

    def add_wire(self, x, y):
        self.wiring.append((x, y))


class Netlist():
    
    def __init__(self, netlist_path: str, print0_path: str):
        
        # load the data from the csv
        df = pd.read_csv(netlist_path)
        self.nets = [(net['chip_a'], net['chip_b']) for idx, net in df.iterrows()]
        
        
    def get_wire_count(self):
        return sum(len(net.wiring for net in self.nets))