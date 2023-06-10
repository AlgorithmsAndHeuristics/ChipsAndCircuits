import pandas as pd

class Net():
    
    def __init__(self, chip_a, chip_b):
        self.gates = [chip_a, chip_b]
        self.wiring = []



class Netlist():
    
    def __init__(self, netlist_path: str, print0_path: str):
        
        # load the data from the csv
        df = pd.read_csv(netlist_path)
        self.nets = [(net['chip_a'], net['chip_b']) for idx, net in df.iterrows()]
        
        
