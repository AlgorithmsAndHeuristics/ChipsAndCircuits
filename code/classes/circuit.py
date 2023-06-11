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
        

        # Create the grid based on the furthest gates
        grid_width = max([gate.position[0] for gate in self.gates])
        grid_height = max([gate.position[1] for gate in self.gates])
        self.grid = [['_' for i in range(grid_width - 1)] for y in range(grid_height + 1)]
        
        # Place the gates on the grid
        for gate in self.gates:
          self.grid[gate.position[0] - 1][gate.position[1] - 1] = gate.id
    
    
    def get_representation(self) -> str:  
        board_str = ""

        for row in self.grid:
            for tile in row:
                board_str += str(tile)

            board_str += "\n"

        return(board_str)
    
    
    
    def load_netlist(self, path: str) -> None:
        self.netlists.append(Netlist(path))
