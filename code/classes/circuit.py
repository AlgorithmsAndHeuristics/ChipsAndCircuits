from gate import Gate
from netlist import Netlist
import pandas as pd


class Circuit():
  
    def __init__(self):
        pass
    
    
    def get_representation(self) -> str:
        pass
    
    
    def load_gates(self, path: str) -> None:
        pass
    
    
    def load_netlist(self, path: str) -> None:
        self.netlists.append(Netlist(path))
