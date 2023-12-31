from gate import Gate
from netlist import Netlist
from net import Net
from wire import Wire
import pandas as pd
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MaxNLocator

Position = tuple[int, int]


class Circuit():
    
    def __init__(self, print_path: str, border: int = 0) -> None:
        """
        PRE: The path to the print_x.csv file of a chip and a growth factor
        POST: Initializes a Circuit object"""

        self.netlists: list[Netlist] = []
        self.gates: dict[int, Gate] = {}
        self.gate_positions: list[tuple[int, int]] = []
        self.border: int = border

        print_x = pd.read_csv(print_path)
        
        # Read the gates from the print_x file
        for index, gate in print_x.iterrows():
            self.gates[int(gate[0])] = (Gate(int(gate[0]), (int(gate[1]), int(gate[2]))))
            self.gate_positions.append((gate[1], gate[2]))


    def any_intersections(self, netlist_id: int, net_id: int = None) -> bool:
        """
        Check if there are any intersections.

        PRE: netlist_id of type int
        POST: returns False if there aren't any intersections,
        else True
        """

        # Check if this net is overlapping any gates
        if net_id != None:
            net: Net = self.get_net(net_id)
            wiring: list[Wire] = net.wiring
            check_set = self.gate_positions

            for wire in wiring:
                # If a wire is on a gate it's an intersection, thus return True
                if (wire.x, wire.y) in check_set:
                    # Check if not net's own gates
                    if (wire.x, wire.y) != net.gates[0].position and (wire.x, wire.y) != net.gates[1].position:
                        return True

        netlist = self.netlists[netlist_id  - 1]
        
        # No intersections if list is empty
        if len(netlist.get_intersections()) == 0:
            return False
        
        return True


    def check_position(self, position: Position, netlist_id: int, net_id: int) -> list[bool]:
        """
        Say something about given position:
        1. Is it an already used position by this net
        2. Is it on a border
        3. Is it on a gate not from this net
        4. Is it on a wire from another net

        PRE: x and y coördinates of a position on the grid
        POST: Returns a triple of booleans respectively 
        representing whether the spot contains a border, Gate or Wire"""

        bool_set = []
        
        # Check if position isn't already used by Wire in Net
        net = self.get_net(net_id)
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
        net: Net = self.get_net(net_id)
        end_gate: Gate = net.gates[-1]
        end_position = end_gate.position

        if (position != end_position and
            position in [(self.gates[gate_id].position[0], self.gates[gate_id].position[1]) for gate_id in self.gates]
            ):
            bool_set.append(True)
        else:
            bool_set.append(False)

        # Check if position contains a Wire
        if position in [(wire.x, wire.y, wire.z) for netlist in self.netlists for net_id in netlist.nets for wire in netlist.nets[net_id].wiring]:
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

        net: Net = self.get_net(net_id)
        end_gate: Gate = net.gates[-1]
        end_position = end_gate.position

        if end_gate in possible_pos:
            self.lay_wire(netlist_id, net_id, end_position)
            return True

        return False
    
            
    def get_gate_entrances(self, gate: Gate) -> list[tuple[int, int, int]]:
        """
        Get the unused entrances of a gate. An entrance
        is given in relative coordinates to that gate.

        PRE: gate of type Gate
        POST: list of entrances of type tuple[int, int, int]
        """

        # State the possible entrances
        possible_entrances: list[tuple[int, int, int]] = [
            (0, 0, 1),
            (1, 0, 0),
            (0, 1, 0),
            (-1, 0, 0),
            (0, -1, 0)
        ]

        # Check for every net in netlist the gates and used entrances
        netlist: Netlist = self.netlists[0]
        for net in netlist:

            # Check if gate matches one of the gates from this net
            net_gates = net.gates
            if gate in net_gates:

                # Get the gate position
                gate_position = (gate.position[0], gate.position[1], 0)

                # Get index of gate in net.gates, this way we know which wire to look for
                gate_index = net_gates.index(gate)
                if gate_index == 0:
                    # The second wire
                    wire = net.wiring[1]
                else:
                    # The second last wire
                    wire = net.wiring[-2]

                # Make sure it aren't just loose wires
                if self.wires_connected(Wire(gate_position[0], gate_position[1], gate_position[2]), wire):
                    # Get entrance outta there
                    entrance = (wire.x - gate_position[0],
                                wire.y - gate_position[1],
                                wire.z - gate_position[2])
                    possible_entrances.remove(entrance)
        
        return possible_entrances


    def get_gate_position(self, gate_id: int) -> tuple[int, int]:
        """
        Returns requested gate's position.

        PRE: gate_id
        POST: coordinates of type tuple[int, int]
        """

        return self.gates[gate_id].position


    def get_net(self, net_id: int) -> Net:
        """
        Returns requested net.
        
        PRE: netlist_id and net_id of type int
        POST: Net object
        """

        # Always 1 netlist in netlists
        return self.netlists[0].nets[net_id - 1]
    

    def get_net_start(self, netlist_id: int, net_id: int) -> tuple[int, int]:
        """
        Get starting position of a net in netlist, 
        i.e. first gate position

        PRE: netlist_id and net_id of type int
        POST: coordinates of type tuple[int, int]
        """

        # Get Net (by ID) in Netlist (by ID) to use as starting point
        net: Net = self.get_net(net_id)
        
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
        
        net: Net = self.get_net(net_id)

        # Get end Gate of a Wire from a Net
        end_gate: Gate = self.gates[net.gates[1].id]
        
        # Check if the last Wire in a Net is the position of the end Gate
        if (net.wiring[-1].x, net.wiring[-1].y) == end_gate.position:

            # Check if the wiring follows a consistent path
            for i in range(0, len(net.wiring) - 1):
                wire1, wire2 = net.wiring[i], net.wiring[i + 1]
                if not self.wires_connected(wire1, wire2):
                    return False
  
            return True

        return False
    

    def load_gate_positions(self) -> None:
        """
        Load all the gate positions into a set.

        POST: self.gate_positions contains all the gate positions
        of type tuple[int, int]
        """

        netlist: Netlist = self.netlists[0]
        for net_id in netlist.nets:
            net: Net = netlist.nets[net_id]
            for gate in net.gates:
                self.gate_positions.add(gate.position)


    def move_level(self, netlist_id: int, net_id: int, n_level: int) -> None:
        """
        Move the wire of requested net from netlist requested amount of levels.

        PRE: netlist_id, net_id and n_level of type int
        POST: line from self.netlists[netlist_id][net_id - 1] 
        is moved n_level layers
        """

        net: Net = self.get_net(net_id)
        wiring: list[Wire] = net.wiring

        # Move all wires except first and list to correct layer
        for wire in wiring[1:-1]:
            wire.z = n_level

        net.wiring = wiring


    def lay_wire(self, netlist_id: int, net_id: int, position: Position) -> None:
        """
        Lay wire on requested net from netlist.

        PRE: netlist_id, net_id, x and y of type int
        POST: wire of type Wire is added to self.netlists[netlist_id][net_id - 1]
        """

        # Fix for z coordinate given
        if len(position) == 3:
            wire = Wire(position[0], position[1], position[2])
        else:
            wire = Wire(position[0], position[1])

        net: Net = self.get_net(net_id)
        net.add_wire(wire)

        
    def lay_from_gate(self, netlist_id: int, net_id: int, position: Position, position_index: int = None) -> None:
        """
        Lay wire on requested net from netlist. If a position index is given,
        that means we have to insert from gate one after 'position_index' wires.

        PRE: netlist_id, net_id and gate_index of type int, and position of type Position
        POST: wire of type Wire is added to self.netlists[netlist_id][net_id - 1]
        """
    
        # Fix for z coordinate given
        if len(position) == 3:
            wire = Wire(position[0], position[1], position[2])
        else:
            wire = Wire(position[0], position[1])

        net: Net = self.get_net(net_id)
        wiring: list[Wire] = net.wiring

        # If from the first gate
        if position_index:
            wiring.insert(position_index, wire)

        else:
            # Insert the wire to add
            wiring.insert(len(wiring) - 1, wire)

        # Save new wiring
        net.wiring = wiring

    def undo_lay_from_gate(self, netlist_id: int, net_id: int, position_index: int = None) -> None:

        net: Net = self.get_net(net_id)
        wiring: list[Wire] = net.wiring

        # If from the first gate
        if position_index:
            del wiring[position_index]

        # Delete last added wire
        else:
            del wiring[-2]

        # Save new wiring
        net.wiring = wiring

    def list_shortest_distance(self, netlist_id: int) -> list[int]:
        """
        Sort the gate distances of the nets from shortest to longest.

        PRE: netlist_id of type int
        POST: list[netlist_id] where netlist_id is of type int
        """

        netlist = self.netlists[netlist_id - 1]
        distances = netlist.direct_distances()
        # sort on the second value i.e. distance of the distances list,
        # and put only the net_id in the list.
        return [i for i, j in sorted(distances, key=lambda x: x[1])]


    def most_connected_nets(self, netlist_id: int) -> list[int]:
        """
        Sort the netlist on most connected gates.

        PRE: netlist_id of type int
        POST: list with integers representing net_id's
        """

        netlist = self.netlists[netlist_id - 1]
        nets: dict[int, Net] = netlist.nets
        connections = netlist.gate_connections()

        # Sort the gates on n connections
        gates = [i for i, j in sorted(connections.items(), key=lambda x: x[1], reverse=True)]

        sorted_nets: list[Net] = []
        for gate in gates:
            for net_id in nets:
                if nets[net_id].gates[0].id == gate:
                    sorted_nets.append(net_id)

        return sorted_nets
                    


    def most_connected_gates(self, netlist_id: int) -> list[list[tuple[int, int]]]:
        """
        Sort gate id on amount of connections, starting from most.

        PRE: netlist_id of type int
        POST: list[gate_id] where gate_id is of type int
        """

        netlist = self.netlists[netlist_id - 1]
        connections = netlist.gate_connections()

        # Sort the gates on n connections
        gates = [i for i, j in sorted(connections.items(), key=lambda x: x[1], reverse=True)]

        # Get net_id's for every gate
        sorted_gate_nets = []
        for gate_id in gates:
            nets = []
            for net_id in netlist.nets:
                gates = netlist.nets[net_id].gates
                gates = (gates[0].id, gates[1].id)
                if gate_id in gates:
                    index_gate_net = gates.index(gate_id)
                    nets.append((net_id, index_gate_net))
            sorted_gate_nets.append(nets)

        return sorted_gate_nets

    
    def load_netlist(self, path: str) -> None:
        """
        PRE: The path to a netlist_x.csv file
        POST: Netlist has been added to self.netlists"""

        self.netlists.append(Netlist(path, self.gates))


    def next_positions(self, netlist_id: int, net_id: int) -> list[tuple[int, int]]:
        """
        Checks valid following coordinates where wire can be placed
        from requested net from netlist.

        PRE: netlist_id and net_id of type int
        POST: list with coordinates of type tuple[int, int]
        """

        net: Net = self.get_net(net_id)

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

        net: Net = self.get_net(net_id)
        net.unadd_wire()


    def plot_grid(self, title: str = "Circuit"):
        """
        Pre: self and a title
        Post: returns a 3D plot representing the gates and wires
        """

        "Make a 3D figure"
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111, projection='3d')

        # add the gates to the plot
        for gate in self.gates.values():
            x, y, z, label = gate.position[0], gate.position[1], 0, gate.id
            ax.scatter(x, y, z, color="red")
            ax.text(x, y, z + 0.2, label, ha='center', va='bottom')

        plot_handles = []
        plot_labels = []
        
        # Get the wire coördinates per net
        for net in self.netlists[0].nets.values():
            x = [wire.x for wire in net.wiring]
            y = [wire.y for wire in net.wiring]
            z = [wire.z for wire in net.wiring]
            line, = ax.plot(x, y, z)
            
            # Add the net descriptions to the first legend
            plot_handles.append(line)
            plot_labels.append(f'Gate {net.gates[0].id} to {net.gates[1].id}')

        # Add the first legend
        legend_1 = plt.legend(plot_handles, plot_labels, loc='upper right', bbox_to_anchor=(0, 1), ncol = 2)
        plt.gca().add_artist(legend_1)

        # Make descriptive labels and placeholder handles for the second legend
        plot_labels2 = []
        plot_labels2.append(f"Gate count: {len(self.gates)}")
        plot_labels2.append(f"Net count: {len(self.netlists[0].nets.values())}")
        plot_labels2.append(f"Wire count: {self.netlists[0].get_wire_count()}")
        plot_labels2.append(f"Intersection count: {len(self.netlists[0].get_intersections())}")
        plot_labels2.append("")
        plot_labels2.append(f"Netlist cost: {self.netlists[0].get_cost()}")
        plot_handles2 = [line for i in range(len(plot_labels2))]

        # Add the second legend
        plt.legend(plot_handles2, plot_labels2, loc='lower right', bbox_to_anchor=(1.4, 0.6), handlelength=0)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(title)
        
        # Limit the Z-axys and only take steps of 1
        ax.set_zlim(0, 4)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True, steps=[1]))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True, steps=[1]))
        ax.zaxis.set_major_locator(MaxNLocator(integer=True, steps=[1]))

        plt.show()


    def wires_connected(self, wire1: Wire, wire2: Wire) -> bool:
        """
        Check if two wires are connected

        PRE: wire1 and wire2 of type Wire
        POST: True if wires are connected, else False
        """

        if (
            not 
        (abs(wire1.x - wire2.x) == 1 and 
            abs(wire1.y - wire2.y) == 0 and 
            abs(wire1.z - wire2.z) == 0) and
        not 
        (abs(wire1.x - wire2.x) == 0 and 
            abs(wire1.y - wire2.y) == 1 and 
            abs(wire1.z - wire2.z) == 0) and
        not 
        (abs(wire1.x - wire2.x) == 0 and 
            abs(wire1.y - wire2.y) == 0 and 
            abs(wire1.z - wire2.z) == 1)
        ):
            return False
        return True
    

    def __getstate__(self):
        """
        Return a dictionary of the Circuit's state."""
        
        return {'netlists': self.netlists, 'gates': self.gates, 
                'gate_positions': self.gate_positions, 'border': self.border}


    def __setstate__(self, state):
        """
        Restore the Circuit's state from the state dictionary."""

        self.netlists = state['netlists']
        self.gates = state['gates']
        self.gate_positions = state['gate_positions']
        self.border = state['border']
