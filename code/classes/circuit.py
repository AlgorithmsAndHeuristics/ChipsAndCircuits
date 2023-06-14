from gate import Gate
from netlist import Netlist
from net import Net
from wire import Wire
import pandas as pd
import math
import matplotlib.pyplot as plt

Position = tuple[int, int]


# TODO: self.layers
class Circuit():
    
    def __init__(self, print_path: str, border: int = 8) -> None:
        """
        PRE: The path to the print_x.csv file of a chip and a growth factor
        POST: Initializes a Circuit object"""

        self.netlists: list[Netlist] = []
        self.netlists2: dict[int, Netlist] = dict()
        self.gates: dict[int, Gate] = {}
        self.border: int = border

        print_x = pd.read_csv(print_path)
        
        # Read the gates from the print_x file
        for index, gate in print_x.iterrows():
            self.gates[int(gate[0])] = (Gate(int(gate[0]), (int(gate[1]), int(gate[2]))))
        

    def plot_grid(self) -> str:  

        # Extract x, y, and names from the points list
        x = [gate.position[0] for gate in self.gates.values()]
        y = [gate.position[1] for gate in self.gates.values()]
        names = [gate.id for gate in self.gates.values()]

        fig, ax = plt.subplots()

        # Plot the gates in red
        ax.plot(x, y, 'ro')

        # Add name annotations
        for i, name in enumerate(names):
            ax.annotate(name, (x[i], y[i]), textcoords="offset points", xytext=(0, 10), ha='center')

        # Set the labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Layer 1')

        # Add the wires
        for netlist in self.netlists:
            for index, net in enumerate(netlist.nets2.values()):
                

                for i in range(len(net.wiring)):
                    if i != len(net.wiring) - 1:
                        start = (net.wiring[i].x, net.wiring[i].y)
                        end = (net.wiring[i+1].x, net.wiring[i+1].y)
                        ax.plot([start[0] , end[0]], [start[1], end[1]], 
                                ['b-', 'r-', 'g-', 'c-', 'm-', 'y-'][index])                    

        # add borders
        for border in [((-1,-1), (-1,8)),((-1,-1), (8,-1)), ((-1,8), (8,8)), ((8,-1), (8,8))]:
            start_point = border[0]
            end_point = border[1]
            ax.plot([start_point[0] , end_point[0]], [start_point[1], end_point[1]], 'k-')

        # Show the grid
        plt.grid(True)

        # Display the plot
        return plt.show()

    
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
        if position[0] < 0 or position[0] >= self.border or position[1] < 0 or position[1] >= self.border:
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

    
    def get_gate_position(self, gate_id: int) -> tuple[int, int]:
        """
        Returns requested gate's position.

        PRE: gate_id
        POST: coordinates of type tuple[int, int]
        """

        return self.gates[gate_id].position


    def get_net(self, netlist_id: int, net_id: int) -> Net:
        """
        Returns requested net.
        
        PRE: netlist_id and net_id of type int
        POST: Net object
        """

        return self.netlists[netlist_id - 1].nets2[net_id - 1]
    

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
    
    
    def load_netlist(self, path: str) -> None:
        """
        PRE: The path to a netlist_x.csv file
        POST: Netlist has been added to self.netlists"""

        self.netlists.append(Netlist(path, self.gates))
    

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


    def undo_lay(self, netlist_id: int, net_id: int) -> None:
        """
        Undo last lay of wire on requested net from netlist.

        PRE: netlist_id and net_id of type int
        POST: wire is removed from self.netlists[netlist_id][net_id - 1]
        """

        net: Net = self.get_net(netlist_id, net_id)
        net.unadd_wire()
