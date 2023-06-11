from gate import Gate
from netlist import Netlist
import pandas as pd


class Circuit():
  
    def __init__(self, print_path):
        self.netlists: list[Netlist] = []
        self.gates: list[Gate] = []
        
        print_x = pd.read_csv(print_path)
        
        # Read the gates from the print_x file
        for index, gate in print_x.iterrows():
          self.gates.append(Gate(int(gate[0]), (int(gate[1]), int(gate[2]))))
          
    
    
    def get_representation(self) -> str:
        pass
    
    
    def load_gates(self, path: str) -> None:
        pass
    
    
    def load_netlist(self, path: str) -> None:
        self.netlists.append(Netlist(path))
