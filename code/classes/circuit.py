from gate import Gate
from netlist import Netlist
import pandas as pd


# TODO: self.layers
class Circuit():
    
    def __init__(self, print_path: str, factor: int = 1) -> None:
        self.netlists: list[Netlist] = []
        self.gates: list[Gate] = []
        
        print_x = pd.read_csv(print_path)
        self.cell_width: int = 1
        
        # Read the gates from the print_x file
        for index, gate in print_x.iterrows():
            self.gates.append(Gate(int(gate[0]), (int(gate[1]), int(gate[2]))))
            
            # Determine cell width by getting the gate coordinate with the longest length
            gate_x_len: int = len(str(gate[1]))
            gate_y_len: int = len(str(gate[2]))
            
            if gate_x_len > self.cell_width:
                self.cell_width = gate_x_len
            
            if gate_y_len > self.cell_width:
                self.cell_width = gate_y_len
        
        self.make_grid(factor)

    
    def __repr__(self) -> str:  
        board_str = ""
        board = self.grid

        # Place the wires on the board
        for netlist in self.netlists:
            for net in netlist.nets:
                for wire in net.wiring:
                    board[wire.y - 1][wire.x - 1] = "."

        # Place the intersections on the board
        for netlist in self.netlists:
            for intersection in netlist.get_intersections():
                board[intersection.y - 1][intersection.x - 1] = "x"
        
        # Turn the board into a string
        for row in board:
            for tile in row:
                board_str += str(tile)

            board_str += "\n"

        return board_str
    

    def get_gate_id(self, gate: Gate) -> str:
        gate_id: str = str(gate.id)
        
        # For each digit that a gate ID is shorter than cell width, append a whitespace character
        if self.cell_width > len(gate_id):
            for _ in range(self.cell_width - len(gate_id)):
                gate_id += ' '
        
        return gate_id
    
    
    def get_underscore(self) -> str:
        underscore: str = '_'
        
        if self.cell_width > 1:
            for _ in range(self.cell_width - 2):
                underscore += '_'
            
            underscore += ' '
        
        return underscore
    
    
    def load_netlist(self, path: str) -> None:
        self.netlists.append(Netlist(path))
    
    
    def make_grid(self, factor: int) -> None:
        """
        Make the grid with a multiplying factor.
        PRE: Factor of type int, must be larger or equal to 1
        POST: Grid is dimensions are multiplied by factor,
        center stays the same"""

        assert factor >= 1, "Can't make grid smaller than biggest distance"

        # Set characters based on cell width
        underscore: str = self.get_underscore()
        
        # Create the grid based on the furthest gates
        org_width = max([gate.position[0] for gate in self.gates])
        org_height = max([gate.position[1] for gate in self.gates])
        
        grid_width = int(org_width * factor)
        grid_height = int(org_height * factor)
        
        self.grid: list[list[str]] = [[underscore for y in range(grid_height + 1)] for x in range(grid_width + 1)]
        
        # Place the gates on the grid
        x_move = (grid_width - org_width) // 2
        y_move = (grid_height - org_height) // 2

        for gate in self.gates:
            gate.position = (gate.position[0] + x_move, gate.position[1] + y_move)
            self.grid[gate.position[0] - 1][gate.position[1] - 1] = self.get_gate_id(gate)
