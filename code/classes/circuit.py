from gate import Gate
from netlist import Netlist
from net import Net
from wire import Wire
import pandas as pd
import math


# TODO: self.layers
class Circuit():
    
    def __init__(self, print_path: str, factor: int = 1) -> None:
        """
        PRE: The path to the print_x.csv file of a chip and a growth factor
        POST: Initializes a Circuit object"""

        self.netlists: list[Netlist] = []
        self.gates: dict[int, Gate] = {}
        
        print_x = pd.read_csv(print_path)
        
        # Read the gates from the print_x file
        for index, gate in print_x.iterrows():
            self.gates[int(gate[0])] = (Gate(int(gate[0]), (int(gate[1]), int(gate[2]))))
        
        self.make_grid(factor)
    

    def make_grid(self, factor: int) -> None:
        """
        Make the grid with a multiplying factor.
        PRE: Factor of type int, must be larger or equal to 1
        POST: Grid is dimensions are multiplied by factor,
        center stays the same"""

        assert factor >= 1, "Can't make grid smaller than minimum distance"

        # Create the grid based on the furthest gates
        org_width = max([self.gates[id].position[0] for id in self.gates])
        org_height = max([self.gates[id].position[1] for id in self.gates])
        grid_width = int(org_width * factor)
        grid_height = int(org_height * factor)
        self.grid = [['_' for i in range(grid_width + 1)] for y in range(grid_height + 1)]
        
        # Place the gates on the grid
        x_move = (grid_width - org_width) // 2
        y_move = (grid_height - org_height) // 2

        for id in self.gates:
            gate = self.gates[id]
            gate.position = (gate.position[0] + x_move, gate.position[1] + y_move)
            self.grid[gate.position[1]][gate.position[0]] = gate.id

    def __repr__(self) -> str:  
        board_str = ""
        board = self.grid

        # Place the wires on the board
        for netlist in self.netlists:
            for net in netlist.nets:
                for wire in net.wiring:
                    board[wire.y - 1][wire.x - 1] = "-"

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
    
    
    def load_netlist(self, path: str) -> None:
        """
        PRE: The path to a netlist_x.csv file
        POST: Netlist has been added to self.netlists"""

        self.netlists.append(Netlist(path, self.gates))

    
    def check_position(self, x: int, y: int) -> set[bool]:
        """
        PRE: x and y coördinates of a position on the grid
        POST: Returns a triple of booleans respectively 
        representing whether the spot contains a border, Gate or Wire"""

        bool_set = ()

        # Check if position contains a border (are out of bounds)
        if x < 0 or x > len(self.grid[0]) or y < 0 or y > len(self.grid):
            bool_set.add(True)
        else:
            bool_set.add(False)

        # Check if position contains a gate
        if (x, y) in [(gate.position[0], gate.position[1]) for gate in self.gates]:
            bool_set.add(True)
        else:
            bool_set.add(False)

        # Check if position contains a wire
        if (x,y) in [(wire.x, wire.y) for netlist in self.netlists for net in netlist.nets for wire in net.wiring]:
            bool_set.add(True)
        else:
            bool_set.add(False)

        return bool_set


    def get_net(self, netlist_id: int, net_id: int) -> Net:
        """
        Returns requested net.
        
        PRE: netlist_id and net_id of type int
        POST: Net object
        """

        return self.netlists[netlist_id - 1].nets[net_id - 1]

    
    def get_gate_position(self, gate_id: int) -> tuple[int, int]:
        """
        Returns requested gate's position.

        PRE: gate_id
        POST: coordinates of type tuple[int, int]
        """

        return self.gates[gate_id].position
    

    def get_net_start(self, netlist_id: int, net_id: int) -> tuple[int, int]:
        """
        Get starting position of a net in netlist, 
        i.e. first gate position

        PRE: netlist_id and net_id of type int
        POST: coordinates of type tuple[int, int]
        """

        net: Net = self.get_net(netlist_id, net_id)
        gate: Gate = net.gates[0]
        return self.get_gate_position(gate.id)

    def is_connected(self, netlist_id: int, net_id: int) -> bool:
        """
        Check if requested netlist is connected.
        If first and last wires in the wire list of the net
        are equal in coordinates of the gates returns True,
        else False.

        PRE: netlist_id and net_id of type int
        POST: True or False
        """
        
        netlist = self.netlists[netlist_id - 1]
        net = netlist.nets[net_id - 1]
        gate_1, gate_2 = self.gates[net.gates[0].id], self.gates[net.gates[1].id]
        
        if ((net.wiring[0].x, net.wiring[0].y) == gate_1.position and
            (net.wiring[-1].x, net.wiring[-1].y) == gate_2.position
        ):
            return True
        
        return False
    
    def lay_wire(self, netlist_id: int, net_id: int, x: int, y: int) -> None:
        """
        Lay wire on requested net from netlist.

        PRE: netlist_id, net_id, x and y of type int
        POST: wire of type Wire is added to self.netlists[netlist_id][net_id - 1]
        """

        wire = Wire(x, y)
        net: Net = self.get_net(netlist_id, net_id - 1)
        net.add_wire(wire)

    def undo_lay(self, netlist_id: int, net_id: int) -> None:
        """
        Undo last lay of wire on requested net from netlist.

        PRE: netlist_id and net_id of type int
        POST: wire is removed from self.netlists[netlist_id][net_id - 1]
        """

        net: Net = self.get_net(netlist_id, net_id - 1)
        net.unadd_wire()

    def next_positions(self, netlist_id: int, net_id: int) -> list[tuple[int, int]]:
        """
        Checks valid following coordinates where wire can be placed
        from requested net from netlist.

        PRE: netlist_id and net_id of type int
        POST: list with coordinates of type tuple[int, int]
        """

        net: Net = self.get_net(netlist_id, net_id - 1)
        last_wire: Wire = net.wiring[-1]

        possible_positions = [(last_wire.x + ix, last_wire.y + iy)
                               for ix in range(-1, 2, 2)
                               for iy in range(-1, 2, 2)]
        
        viable_positions = []
        for position in possible_positions:
            bool_set = self.check_position(position[0], position[1])
            if bool_set[0] == False and bool_set[1] == False:
                viable_positions.append(position)

        return viable_positions