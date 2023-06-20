from code.classes.circuit import Circuit

import random

Position = tuple[int, int]
Directions = list[Position]


# REAL NET_ID GET'S USED HERE
def make_wire(circuit: Circuit, netlist_id: int, net_id: int):
    """
    Wire the net by randomly choosing valid coordinates
    to go to one by one. If a wire gets stuck, go one iter back.
    Repeat until the gates are connected i.e.
    """

    print("-"*15)
    net = circuit.get_net(netlist_id, net_id)
    print(f"\nDOING: Gate {net.gates[0]} to Gate {net.gates[1]}")
    #print(f">CIRCUIT NOW:\n\n{circuit}")


    # If Wire is connected between the Gates of the Net it's done
    if circuit.is_connected(netlist_id, net_id):
        return circuit

    # Get viable next possible positions from last Wire in Wire list of the Net
    positions: list[Position] = circuit.next_positions(netlist_id, net_id)

    # If second's Gate position is in possible positions, just go to it by laying Wire
    if circuit.connect_gate(positions, netlist_id, net_id):
        return circuit

    random.shuffle(positions)
    print(f">POSSIBLE POSITIONS: {positions}\n")

    # Go off every position (if there are) until connection is found
    for position in positions:

        print(f">CHOSE: {position}\n")

        circuit.lay_wire(netlist_id, net_id, position)

        # Done if rest of the wiring deems succesful
        if make_wire(circuit, netlist_id, net_id):
            return circuit
        
        # Not found so remove last Wire
        circuit.undo_lay(netlist_id, net_id)

    return None


def make_nets(circuit: Circuit, netlist_id: int):

    # Get requested netlist and make list of all net id's 
    # netlist_id - 1 CURRENTLY NOT ALWAYS CORRECT, 
    # netlist_id goes above 2, and only one netlist is always added anyways (see representation.py)
    print("\n-------START-------")
    netlist = circuit.netlists[netlist_id - 1]

    # Create list of Net IDs from a Netlist
    r_list = list(range(len(netlist.nets)))

    # ipv list[Net] dict[int, Net], waarbij int net ID is en Net het object

    random.shuffle(r_list)

    for net_id in r_list:
        # id of net in netlist is id in csv - 1 ... fix
        net_id += 1
        
        # Get starting position based on Net (by ID) in a Netlist (by ID)
        starting_position: Position = circuit.get_net_start(netlist_id, net_id)

        print(f"netlist_id={netlist_id} | net_id={net_id - 1} | start_pos={starting_position}")

        # place first coordinate (of gate, so shouldn't count as wire!) 
        # shouldn't already be done somewhere else?
        circuit.lay_wire(netlist_id, net_id, starting_position)

        # Make the wire connect to the last gate
        circuit = make_wire(circuit, netlist_id, net_id)


        print("-------DONE-------\n")
