"""
HEURISTICS:
'LAYER INFLUENCED'
>> Assumption: better off playing with layers and always keeping shortest distance (x&y)
1. Start with the shortest distances 
>> Assumption: larger ones are most interfering
LOOP:
2. Lay a straight line, try on plane z=0 first
>> Assumption: straight line is best option
3. If intersection encountered, start again and move a plane up on first step
4. If intersection encountered, start again and move a plane down on first step
5. If intersection encountered, start again and move two planes up on first step
6. etc etc
"""

import random
import os
import sys

directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(directory)
sys.path.append(os.path.join(parent_directory, "classes"))

from circuit import Circuit
from net import Net
from gate import Gate
from wire import Wire

Position = tuple[int, int, int]

def lay_shortest_line(circuit: Circuit, netlist_id: int, net_id: int):
    """
    Connect the gates in requested net from netlist with (one of the) the shortest line(s).
    x & y are not always same length, so method is to +1 them equally first,
    until one is completed, and then finish either one.

    PRE: netlist_id and net_id of type int
    POST: Gates from self.netlists[netlist_id][net_id - 1] are
    connected with the shortest line
    """

    net: Net = circuit.get_net(netlist_id, net_id)
    gates: tuple[Gate, Gate] = net.gates
    position = gates[0].position
    end_position = gates[1].position

    # Direction for x
    if position[0] < end_position[0]:
        x_direction = 1
    else:
        x_direction = -1

    # Direction for y
    if position[1] < end_position[1]:
        y_direction = 1
    else:
        y_direction = -1

    # Var for axis switch, x = 1 / y = -1
    axis = 1

    while True:
        wire = Wire(position[0], position[1], 0)
        net.add_wire(wire)

        # If last added wire was not end_position, make new position
        if position != end_position:
            # Create position for x axis if it isn't already on end position
            if axis == 1:
                if position[0] != end_position[0]:
                    position = (position[0] + x_direction, position[1])
                else:
                    position = (position[0], position[1] + y_direction)

                # Only switch axis if that axis isn't already on end position
                if position[1] != end_position[1]:
                    axis = -1

                continue

            # Create position for y axis
            else:
                if position[1] != end_position[1]:
                    position = (position[0], position[1] + y_direction)
                else:
                    position = (position[0] + x_direction, position[1])

                if position[0] != end_position[0]:
                    axis = 1

                continue

        else:
            break

    return circuit


def layer_line(circuit: Circuit, netlist_id: int, net_id: int) -> Circuit:
    """
    Check if the straight line has no intersections. If it does,
    try to move a plane up first i.e. same line but
    first move up last move down. If another intersection is encountered,
    try to move a plane down. Loop this with adding a layer
    everytime until no intersections encountered.

    PRE: circuit of type Circuit, netlist_id and net_id of type int
    POST: circuit of type Circuit
    """

    n_level: int = 1

    while True:
        print(f"NET: {circuit.get_net(netlist_id, net_id)}")

        # Check if no intersections
        if not circuit.any_intersections(netlist_id):
            print("\nNO INTERSECTIONS")
            break
        
        print(f"\nINTERSECTION, MOVING TO LEVEL {n_level}")
        # Move a level
        circuit.move_level(netlist_id, net_id, n_level)

        # Go to next layer
        n_level += 1

    return circuit


def manhattan_line_x(circuit: Circuit, netlist_id: int, net_id: int, start_position: Position, end_position: Position) -> Circuit:
    """

    """

    # Get directions and distances, order is x then y
    directions, distances = [], []
    for i in range(2):
        distance = end_position[i] - start_position[i]
        if distance == 0:
            directions.append(0)
            distances.append(0)
        else:
            direction = int(distance / abs(distance))
            directions.append(direction)
            distances.append(abs(distance))


    # X is always first priority
    priority_order = [0, 1]

    for priority in priority_order:
        # If distance in this direction is not zero
        if distances[priority] != 0:
            new_start_position = list(start_position)
            new_start_position[priority] += directions[priority]
            new_start_position = tuple(new_start_position)

            # Check if the new position is the end position, if so return the circuit
            # this way it doesn't get added
            if new_start_position == end_position:
                return circuit

            circuit.lay_wire(netlist_id, net_id, new_start_position)

            # Check for intersections, if any undo lay and return None
            if circuit.any_intersections(netlist_id):
                
                circuit.undo_lay(netlist_id, net_id)
                return None
            # Else go on with recursion
            else:
                if manhattan_line_x(circuit, netlist_id, net_id, new_start_position, end_position):
                    return circuit
                
                circuit.undo_lay(netlist_id, net_id)

    # Return None if no path could be found
    return None


def intitial_lines(circuit: Circuit, netlist_id: int, sorted_nets: list[int]):
    """
    Lay the initial lines following the heuristics:
    1. lay one of the shortest line possible between the gates
    2. if this line intersects with another net, move it layers up until
    it doesn't intersect with any other net.
    """

    for net_id in sorted_nets:
        
        print(f"\nDOING: netlist_id={netlist_id} | net_id={net_id + 1}")
        net_id += 1
        net: Net = circuit.get_net(netlist_id, net_id)
        
        # Get initial positions
        start_position = net.gates[0].position
        end_position = net.gates[1].position

        # Fix for gate position, which doesn't have z coordinate
        start_position = (start_position[0], start_position[1], 0)
        end_position = (end_position[0], end_position[1], 0)
        end_gate = end_position

        # Make sure first gate is added SKIP
        circuit.lay_wire(netlist_id, net_id, start_position)

        # Do until a line is layed succesfully
        while True:

            new_circuit = manhattan_line_x(circuit, netlist_id, net_id, start_position, end_position)

            # Failed to make manhattan line on this layer
            if new_circuit == None:
                # Go a layer up
                print(f"\n LAYER UP")
                start_position = (start_position[0], start_position[1], start_position[2] + 1)
                end_position = (end_position[0], end_position[1], end_position[2] + 1)
                continue
            else:
                # Add last gate position then stop SKIP
                new_circuit.lay_wire(netlist_id, net_id, end_gate)
                
                break

    return new_circuit


def manhattan_line_up(circuit: Circuit, netlist_id: int, net_id: int, start_position: Position, end_position: Position, position_index: int = None, gate_pos: int = None) -> Circuit:
    """

    """

    # Get directions and distances, order is x to y to z
    directions, distances = [], []
    for i in range(3):
        distance = end_position[i] - start_position[i]
        if distance == 0:
            directions.append(0)
            distances.append(0)
        else:
            direction = int(distance / abs(distance))
            directions.append(direction)
            distances.append(abs(distance))


    # If Z direction is possible, prioritize it, else choose randomly between x and y
    if distances[2] != 0:
        xy_priority = [0, 1]
        random.shuffle(xy_priority)
        priority_order = [2] + xy_priority
    else:
        priority_order = [0, 1]
        random.shuffle(priority_order)

    print(f"\nOPTIONS: dis = {distances} - prio = {priority_order}")
    for priority in priority_order:
        # If distance in this direction is not zero
        if distances[priority] != 0:
            new_start_position = list(start_position)
            new_start_position[priority] += directions[priority]
            new_start_position = tuple(new_start_position)

            # Check if the new position is the end position, if so return the circuit
            # this way it doesn't get added
            print(f"IF: {new_start_position} - {end_position}")
            if new_start_position == end_position:
                return circuit

            print(f"\nLAY {new_start_position}")
            circuit.lay_from_gate(netlist_id, net_id, new_start_position, position_index)

            # Check for intersections, if any undo lay and return None
            # in case of starting at gate, that position is also invalid
            if circuit.any_intersections(netlist_id) or gate_pos == new_start_position:
                print("\nINTERSECTION ENCOUNTERED, UNDO LAY")
                circuit.undo_lay_from_gate(netlist_id, net_id, position_index)
                continue
            
            # Else go on with recursion
            else:
                if position_index != None:
                    if manhattan_line_up(circuit, netlist_id, net_id, new_start_position, end_position, position_index + 1, gate_pos):
                        return circuit
                else:
                    if manhattan_line_up(circuit, netlist_id, net_id, new_start_position, end_position, None, gate_pos):
                        return circuit
                    
                if position_index != None:
                    circuit.undo_lay_from_gate(netlist_id, net_id, position_index)
                else:
                    circuit.undo_lay_from_gate(netlist_id, net_id)

    # Return None if no path could be found
    return None  


def connect_all_gates(circuit: Circuit, netlist_id: int, sorted_nets: list[int]):
    """
    Connect all wires that remain unconnected to the gates.
    """

    print(f"\n------CONNECTING GATES------")

    amount = 0
    for net_group in sorted_nets:
        print(f"\nNET GROUP: {net_group}")
        for net_id, index_gate_net in net_group:
            # if amount == 1:
            #     break
            # amount += 1
            
            print(f"\nGATE CHECKING: net_id={net_id + 1} | gate_index{index_gate_net}")
            net_id += 1
            net: Net = circuit.get_net(netlist_id, net_id)

            # Check if already connected
            if circuit.is_connected(netlist_id, net_id):
                print(f"\nGATES ALREADY CONNECTED")
                continue

            # Start position is first gate
            if index_gate_net == 0:

                # Fix for gate position, which doesn't have z coordinate
                start_position = net.gates[0].position
                start_position = (start_position[0], start_position[1], 0)
                gate_pos = start_position
                
                end_position = net.wiring[1]
                end_position = (end_position.x, end_position.y, end_position.z)

                # Get available entrances
                available_entrances = circuit.get_gate_entrances(net.gates[0])

            # End position is last gate
            else:
                start_position = net.wiring[-2]
                start_position = (start_position.x, start_position.y, start_position.z)

                end_position = net.gates[1].position
                end_position = (end_position[0], end_position[1], 0)
                gate_pos = end_position

                available_entrances = circuit.get_gate_entrances(net.gates[1])

            # Get the available entrances to the gate
            for entrance in available_entrances:
                # Add entrance position accordingly
                if index_gate_net == 0:
                    print(f"\nTRYING ENTRANCE FROM FIRST GATE: {entrance}")
                    new_start_position = (start_position[0] + entrance[0], 
                                         start_position[1] + entrance[1], 
                                         start_position[2] + entrance[2])
                    
                    # Add entrance to wiring
                    print(f"\nLAY {start_position}")
                    circuit.lay_from_gate(netlist_id, net_id, new_start_position, 1)
                    
                    new_circuit = manhattan_line_up(circuit, netlist_id, net_id, 
                                                    new_start_position, end_position, 2, gate_pos)
                    
                if index_gate_net == 1:
                    print(f"\nTRYING ENTRANCE FROM LAST GATE: {entrance}")
                    new_end_position = (end_position[0] + entrance[0],
                                      end_position[1] + entrance[1],
                                      end_position[2] + entrance[2])
                    
                    new_circuit = manhattan_line_up(circuit, netlist_id, net_id, 
                                                    start_position, new_end_position, None, gate_pos)

                if new_circuit != None:
                    circuit = new_circuit
                    if index_gate_net == 1:
                        print(f"\nLAY {new_end_position}")
                        circuit.lay_from_gate(netlist_id, net_id, new_end_position)
                    print(f"\nGATE CONNECTED")
                    break
                else:
                    if index_gate_net == 0:
                        circuit.undo_lay_from_gate(netlist_id, net_id, 1)

            # All entrances failed
            if new_circuit == None:
                print("\nFAILED")
                return circuit

        # if amount == 1:
        #     break

    return circuit


def greedy_make_nets(circuit: Circuit, netlist_id: int):
    """
    Go off all nets in netlist in order of distance between it's gates,
    make a straight line, and correct the line if necessary.

    PRE: circuit of type Circuit and netlist_id of type int
    POST: nets from netlist of circuit are connected
    """

    print("\n-------START-------")

    # 1. ORDERING OF NETS
    # Get list of net id's in order of distance between the gates.
    sorted_nets = circuit.list_shortest_distance(netlist_id)

    # 2. UNCOLLIDING LAYERED NETS
    circuit = intitial_lines(circuit, netlist_id, sorted_nets)

    # 3. SORT NETS ON MOST CONNECTIONS FOR CONNECTING GATES
    # >> most collisions possible
    sorted_nets: list[list[tuple[int, int]]] = circuit.most_connected_gates(netlist_id)

    # 4. CONNECTING THE GATES
    circuit = connect_all_gates(circuit, netlist_id, sorted_nets)

    return circuit

