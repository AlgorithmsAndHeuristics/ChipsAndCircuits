import random

from code.classes.circuit import Circuit
from code.classes.net import Net
from code.classes.gate import Gate
from code.classes.wire import Wire

Position = tuple[int, int, int]


def lay_manhattan(circuit: Circuit, netlist_id: int, net_id: int, runTime: int, start_position: Position, end_position: Position) -> Circuit:
    """
    Lay manhattan distance between start and end position. Everytime
    the manhattan directions are not possible, try all other possible directions.
    """
    

    # Get manhattan directions and distances, order is x to y to z
    man_directions, man_distances = [], []
    for i in range(3):
        man_distance = end_position[i] - start_position[i]
        if man_distance == 0:
            man_directions.append(0)
            man_distances.append(0)
        else:
            man_direction = int(man_distance / abs(man_distance))
            man_directions.append(man_direction)
            man_distances.append(abs(man_distance))


    # Get all other possible directions, order is x to y to z
    other_directions = []
    for direction in man_directions:
        # Give both directions in list
        if direction == 0:
            other_directions.append([1, -1])
        # Give opposite direction
        else:
            other_directions.append([direction * -1])

    # Always x or y first, then z
    xy_priority = [0, 1]
    random.shuffle(xy_priority)
    priority_order = xy_priority + [2]

    # Go off priorities for manhattan distance directions
    for priority in priority_order:
        # If distance in this direction is not zero
        if man_distances[priority] != 0:
            new_start_position = list(start_position)
            new_start_position[priority] += man_directions[priority]
            new_start_position = tuple(new_start_position)

            # Check if the new position is the end position, if so return the circuit
            # this way it doesn't get added
            if new_start_position == end_position:
                return circuit
            
            circuit.lay_wire(netlist_id, net_id, new_start_position)

            # Check for intersections, if any undo lay and return None
            # in case of starting at gate, that position is also invalid
            # Also make sure to not go z < 0
            if (circuit.any_intersections(netlist_id) or
                new_start_position[2] < 0
                ):
                circuit.undo_lay(netlist_id, net_id)
                continue

            # Else go on with recursion
            else:
                if lay_manhattan(circuit, netlist_id, net_id, runTime, new_start_position, end_position):
                    return circuit
                    
                # If recursion didn't work undo this lay
                else:
                    circuit.undo_lay(netlist_id, net_id)

    
    # Try again but not manhattan direction
    for priority in priority_order:
        # If distance in this direction is not zero
        for direction in other_directions[priority]:
            new_start_position = list(start_position)
            new_start_position[priority] += direction
            new_start_position = tuple(new_start_position)

            # Check if the new position is the end position, if so return the circuit
            # this way it doesn't get added
            if new_start_position == end_position:
                return circuit
            
            circuit.lay_wire(netlist_id, net_id, new_start_position)

            # Check for intersections, if any undo lay and return None
            # in case of starting at gate, that position is also invalid
            # Also make sure to not go z < 0
            if (circuit.any_intersections(netlist_id) or
                new_start_position[2] < 0
                ):
                circuit.undo_lay(netlist_id, net_id)
                continue

            # Else go on with recursion
            else:
                if lay_manhattan(circuit, netlist_id, net_id, runTime, start_position, end_position):
                    return circuit
                    
                # If recursion didn't work undo this lay
                else:
                    circuit.undo_lay(netlist_id, net_id)


    # Return None if no path could be found
    return None 



def make_nets(circuit: Circuit, netlist_id: int, runTime: int):
    """
    Go off all nets in netlist in order of amount of connections of a gate.

    PRE: circuit of type Circuit and netlist_id and runTime type int
    POST: nets from netlist of circuit are connected
    """

    # 1. ORDERING OF NETS
    #sorted_nets = circuit.list_shortest_distance(netlist_id)
    sorted_nets: list[list[tuple[int, int]]] = circuit.most_connected_nets(netlist_id)

    print(f"\n------CONNECTING GATES------\n")
    for net_id in sorted_nets:

        net_id += 1
        print(f"\nDOING: net_id={net_id}")
        
        # Get start and end position
        gates = circuit.get_net(netlist_id, net_id).gates
        start_position = (gates[0].position[0], gates[0].position[1], 0)
        end_position = (gates[1].position[0], gates[1].position[1], 0)

        # Lay first gate
        circuit.lay_wire(netlist_id, net_id, start_position)

        # Lay manhattan path
        circuit = lay_manhattan(circuit, netlist_id, net_id, runTime, start_position, end_position)

        # Lay last gate
        circuit.lay_wire(netlist_id, net_id, end_position)

        print(f"\nSUCCES: net_id={net_id}")


    print("----ALL NETS ITERATED-------")

    return circuit