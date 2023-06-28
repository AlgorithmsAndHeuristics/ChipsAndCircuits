import random, os, sys

directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(directory)
sys.path.append(os.path.join(parent_directory, "classes"))

from circuit import Circuit

Position = tuple[int, int, int]


def lay_manhattan(circuit: Circuit, netlist_id: int, net_id: int, start_position: Position, end_position: Position, passed_coordinates: list[Position], borders, max_length, recurs_count, count_non_man, max_non_man) -> Circuit:
    """
    Lay manhattan distance between start and end position. Everytime
    the manhattan directions are not possible, try all other possible directions.
    """
    
    # print(f"\n-----------------------------------------------------------TO RECURSION = {recurs_count}")
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

    # print(f"MSTART = {start_position}")
    # Go off priorities for manhattan distance directions
    for priority in priority_order:
        # print(f"MAN TRYING {priority} FROM dis = {man_distances} / dir = {man_directions}")
        # If distance in this direction is not zero
        if man_distances[priority] != 0:
            new_start_position = list(start_position)
            new_start_position[priority] += man_directions[priority]
            new_start_position = tuple(new_start_position)

            # Check if the new position is the end position, if so return the circuit
            # this way it doesn't get added
            if new_start_position == end_position:
                # print("\nSTART=END")
                return circuit
            
            circuit.lay_wire(netlist_id, net_id, new_start_position)

            # Check for intersections, if any undo lay and return None
            # in case of starting at gate, that position is also invalid
            # Also make sure to not go z < 0
            # Also check if new position isn't already passed
            if (circuit.any_intersections(netlist_id, net_id) or
                new_start_position[2] < 0 or
                new_start_position in passed_coordinates or
                len(passed_coordinates) + 1 >= max_length
                ):
                # print(f"\nINTERSECTION: {new_start_position}")
                circuit.undo_lay(netlist_id, net_id)
                continue

            # Check if not on border
            reached_border = False
            for i in range(3):
                border = borders[i]
                for limit in border:
                    if new_start_position[i] == limit:
                        # print(f"\nBORDER REACHED: {new_start_position}")
                        circuit.undo_lay(netlist_id, net_id)
                        reached_border = True
                        break
                if reached_border == True:
                    break
            if reached_border == True:
                continue
                
            # Else go on with recursion
            else:
                # Remember coordinate
                passed_coordinates.append(new_start_position)

                if lay_manhattan(circuit, netlist_id, net_id, new_start_position, end_position, passed_coordinates, borders, max_length, recurs_count + 1, count_non_man, max_non_man):
                    # print(f"\n-----------------------------------------------------------BACK TO RECURSION = {recurs_count}")
                    return circuit
                    
                # If recursion didn't work undo this lay
                else:
                    # print(f"\nRECURSION DIDN'T WORK")
                    circuit.undo_lay(netlist_id, net_id)

                    # Remove coordinate
                    passed_coordinates.remove(new_start_position)

    # Only if under maximum non manhattan path count
    if count_non_man < max_non_man + 1:
        # Make z the priority
        random.shuffle(xy_priority)
        priority_order =  [2] + xy_priority

        # print(f"OSTART = {start_position}")
        # Try again but not manhattan direction
        for priority in priority_order:
            # print(f"OTHER TRYING {priority} FROM dis = {other_directions}")
            # If distance in this direction is not zero
            for direction in other_directions[priority]:
                new_start_position = list(start_position)
                new_start_position[priority] += direction
                new_start_position = tuple(new_start_position)

                # Check if the new position is the end position, if so return the circuit
                # this way it doesn't get added
                if new_start_position == end_position:
                    # print("\nSTART=END")
                    return circuit
                
                circuit.lay_wire(netlist_id, net_id, new_start_position)

                # Check for intersections, if any undo lay and return None
                # in case of starting at gate, that position is also invalid
                # Also make sure to not go z < 0
                if (circuit.any_intersections(netlist_id, net_id) or
                    new_start_position[2] < 0 or
                    new_start_position in passed_coordinates or
                    len(passed_coordinates) + 1 >= max_length
                    ):
                    # print(f"\nINTERSECTION: {new_start_position}")
                    circuit.undo_lay(netlist_id, net_id)
                    continue

                # Check if not on border
                reached_border = False
                for i in range(3):
                    border = borders[i]
                    for limit in border:
                        if new_start_position[i] == limit:
                            # print(f"\nBORDER REACHED: {new_start_position}")
                            circuit.undo_lay(netlist_id, net_id)
                            reached_border = True
                            break
                    if reached_border == True:
                        break
                if reached_border == True:
                    continue

                # Else go on with recursion
                else:
                    # Remember coordinate
                    passed_coordinates.append(new_start_position)

                    if lay_manhattan(circuit, netlist_id, net_id, new_start_position, end_position, passed_coordinates, borders, max_length, recurs_count + 1, count_non_man + 1, max_non_man):
                        # print(f"\n-----------------------------------------------------------BACK TO RECURSION = {recurs_count}")
                        return circuit
                        
                    # If recursion didn't work undo this lay
                    else:
                        # print(f"\nRECURSION DIDN'T WORK")
                        circuit.undo_lay(netlist_id, net_id)

                        # Remove coordinate
                        passed_coordinates.remove(new_start_position)


    # Return None if no path could be found
    return None 



def random_greedy_make_nets(circuit: Circuit, netlist_id: int):
    """
    Go off all nets in netlist in order of amount of connections of a gate.

    PRE: circuit of type Circuit and netlist_id of type int
    POST: nets from netlist of circuit are connected
    """

    # 1. ORDERING OF NETS
    #sorted_nets = circuit.list_shortest_distance(netlist_id)
    sorted_nets: list[list[tuple[int, int]]] = circuit.most_connected_nets(netlist_id)

    # 2. DEFINE BORDERS
    # get max x, y, make depending on that
    borders = [[-4, 27], [-4, 27], [-1, 15]]

    # 3. DEFINE MAX LENGTH
    # make depending on max x, y
    max_length = 34

    #4. DEFINE MAX NON MANHATTAN DIRECTION COUNT
    max_non_man = 4

    # SAVE FAILED NETS
    failed = []

    # print(f"\n------CONNECTING GATES------\n")
    for net_id in sorted_nets:

        net_id += 1
        # print(f"\nDOING: net_id={net_id}")
        
        # Get start and end position
        gates = circuit.get_net(netlist_id, net_id).gates
        start_position = (gates[0].position[0], gates[0].position[1], 0)
        end_position = (gates[1].position[0], gates[1].position[1], 0)

        # Lay first gate
        circuit.lay_wire(netlist_id, net_id, start_position)

        # Remember passed coordinates
        passed_coordinates = [start_position]

        # Lay manhattan path
        new_circuit = lay_manhattan(circuit, netlist_id, net_id, start_position, end_position, passed_coordinates, borders, max_length, 1, 0, max_non_man)

        # No possible path for this wire
        if new_circuit == None:
            failed.append(net_id)
            # print(f"\nFAILED: net_id={net_id}")
            # break if you want to check further here
            return None

        else:
            circuit = new_circuit
            # Lay last gate
            circuit.lay_wire(netlist_id, net_id, end_position)


        # print(f"\nSUCCES: net_id={net_id}")

    # if len(failed) == 0:
    #     print("\n----ALL NETS LINKED-------")
    # else:
    #     print("\n----DONE, BUT FAILED NETS------")
    #     for net_id in failed:
    #         print(f"NET {net_id} FAILED")

    return circuit