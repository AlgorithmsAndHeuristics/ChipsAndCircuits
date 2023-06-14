from gate import Gate
from netlist import Netlist
from net import Net
from wire import Wire
import pandas as pd
import math

Position = tuple[int, int]

# TODO: self.layers
class Circuit():
    
    def __init__(self, print_path: str, factor: int = 1) -> None:
        """
        PRE: The path to the print_x.csv file of a chip and a growth factor
        POST: Initializes a Circuit object"""

        self.netlists: list[Netlist] = []
        self.netlists2: dict[int, Netlist] = dict()
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
        self.grid = [['_' for i in range(grid_width)] for y in range(grid_height)]
        
        # Place the gates on the grid
        x_move = (grid_width - org_width) // 2
        y_move = (grid_height - org_height) // 2

        for id in self.gates:
            gate = self.gates[id]
            gate.position = (gate.position[0] - 1 + x_move, gate.position[1] - 1 + y_move)
            self.grid[gate.position[1]][gate.position[0]] = gate.id


    def __repr__(self) -> str:  
        board_str = ""
        board = self.grid

        # Place the wires on the board
        for netlist in self.netlists:
            for net_id in netlist.nets2:
                for wire in netlist.nets2[net_id].wiring:
                    if board[wire.y][wire.x] == '_':
                        board[wire.y][wire.x] = "-"

        # Place the intersections on the board
        for netlist in self.netlists:
            for intersection in netlist.get_intersections():
                board[intersection.y][intersection.x] = "x"
        
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

    
    def check_position(self, position: Position, netlist_id: int, net_id: int) -> list[bool]:
        """
        PRE: x and y coördinates of a position on the grid
        POST: Returns a triple of booleans respectively 
        representing whether the spot contains a border, Gate or Wire"""

        bool_set = []
        
        # Check if position isn't already used by Wire in Net
        net = self.get_net(netlist_id, net_id)
        wires = net.wiring
        wire_bool = False

        # Check if a Wire of the same Net has already been at that position
        for wire in wires:
            if position == (wire.x, wire.y):
                wire_bool = True
                break
        
        bool_set.append(wire_bool)
        
        # Check if position contains a border (are out of bounds)
        if position[0] < 0 or position[0] > len(self.grid[0]) - 1 or position[1] < 0 or position[1] > len(self.grid) - 1:
            bool_set.append(True)
        else:
            bool_set.append(False)

        # Check if position contains a Gate

        # NOTE: END GATE AS POSITION SHOULD RETURN FALSE:
        net: Net = self.get_net(netlist_id, net_id)
        end_gate: Gate = net.gates[-1]
        end_position = end_gate.position

        if (position != end_position and
            position in [(self.gates[gate_id].position[0], self.gates[gate_id].position[1]) for gate_id in self.gates]
            ):
            bool_set.append(True)
        else:
            bool_set.append(False)

        # Check if position contains a Wire
        if position in [(wire.x, wire.y) for netlist in self.netlists for net_id in netlist.nets2 for wire in netlist.nets2[net_id].wiring]:
            bool_set.append(True)
        else:
            bool_set.append(False)

        return bool_set


    def get_net(self, netlist_id: int, net_id: int) -> Net:
        """
        Returns requested net.
        
        PRE: netlist_id and net_id of type int
        POST: Net object
        """

        return self.netlists[netlist_id - 1].nets2[net_id - 1]

    
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

        # Get Net (by ID) in Netlist (by ID) to use as starting point
        net: Net = self.get_net(netlist_id, net_id)
        
        gate: Gate = net.gates[0]
        return gate.position


    def is_connected(self, netlist_id: int, net_id: int) -> bool:
        """
        Check if requested netlist is connected.
        If first and last wires in the wire list of the net
        are equal in coordinates of the gates returns True,
        else False.

        PRE: netlist_id and net_id of type int
        POST: True or False
        """
        
        net: Net = self.get_net(netlist_id, net_id)

        # Get end Gate of a Wire from a Net
        end_gate: Gate = self.gates[net.gates[1].id]
        
        # Check if the last Wire in a Net is the position of the end Gate
        if (net.wiring[-1].x, net.wiring[-1].y) == end_gate.position:
            return True

        return False
    

    def lay_wire(self, netlist_id: int, net_id: int, position: Position) -> None:
        """
        Lay wire on requested net from netlist.

        PRE: netlist_id, net_id, x and y of type int
        POST: wire of type Wire is added to self.netlists[netlist_id][net_id - 1]
        """

        wire = Wire(position[0], position[1])
        net: Net = self.get_net(netlist_id, net_id)
        net.add_wire(wire)


    def undo_lay(self, netlist_id: int, net_id: int) -> None:
        """
        Undo last lay of wire on requested net from netlist.

        PRE: netlist_id and net_id of type int
        POST: wire is removed from self.netlists[netlist_id][net_id - 1]
        """

        net: Net = self.get_net(netlist_id, net_id)
        net.unadd_wire()


    def next_positions(self, netlist_id: int, net_id: int) -> list[tuple[int, int]]:
        """
        Checks valid following coordinates where wire can be placed
        from requested net from netlist.

        PRE: netlist_id and net_id of type int
        POST: list with coordinates of type tuple[int, int]
        """

        net: Net = self.get_net(netlist_id, net_id)

        # Get last Wire that was laid down
        last_wire: Wire = net.wiring[-1]

        considered_positions = [(last_wire.x + dx, last_wire.y + dy) 
                                for dx, dy 
                                in [(1, 0), (-1, 0), (0, 1), (0, -1)]]

        viable_positions = []
        
        # Iterate over all considered positions
        for position in considered_positions:
            # Get bool set of a considered position
            bool_set = self.check_position(position, netlist_id, net_id)

            # Check if all bools in set are False and the considered position is viable (TODO: use all() if all bools are used, see next comment line)
            # if all(bool_set == False):
            if bool_set[0] == False and bool_set[1] == False and bool_set[2] == False:
                viable_positions.append(position)

        return viable_positions
    

    def connect_gate(self, possible_pos: list[Position], netlist_id: int, net_id: int) -> bool:
        """
        Check if last gate's position is in possible positions,
        if so add the last wire to the requeste net from netlist.

        PRE: possible_pos of type list[tuple[int, int]] and netlist_id and net_id of type int
        POST: if gate position in possible_pos add wire to self.get_net(netlist_id, net_id)
        and return True, else False
        """

        net: Net = self.get_net(netlist_id, net_id)
        end_gate: Gate = net.gates[-1]
        end_position = end_gate.position

        if end_gate in possible_pos:
            self.lay_wire(netlist_id, net_id, end_position)
            print("FOUND LAST++_+_+_+_+_+_+_+_+_+_+_+_+_+_+")
            return True

        return False
