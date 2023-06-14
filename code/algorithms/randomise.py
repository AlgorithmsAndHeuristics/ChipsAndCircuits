from code.classes.circuit import Circuit
from code.classes.netlist import Netlist
from code.classes.net import Net

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

    print(circuit)

    # If wire is connected between the gates of the net it's done
    if circuit.is_connected(netlist_id, net_id):
        return circuit

    # Get next possible positions from last wire in wire list of the net
    positions: list[Position] = circuit.next_positions(netlist_id, net_id)
    

    # Go off every position (if there are) until connection is found
    for position in positions:

        circuit.lay_wire(netlist_id, net_id, position[0], position[1])

        # Done if rest of the wiring deems succesful
        if make_wire(circuit):
            return circuit
        
        # Not found so remove last wire
        circuit.undo_lay()

    return None

def make_nets(circuit: Circuit, netlist_id: int):

    # Get requested netlist and make list of all net id's 
    # netlist_id - 1 CURRENTLY NOT ALWAYS CORRECT, 
    # netlist_id goes above 2, and only one netlist is always added anyways (see representation.py)
    print("\n-------START-------")
    netlist = circuit.netlists[netlist_id - 1]
    r_list = list(range(len(netlist.nets)))
    random.shuffle(r_list)

    for net_id in r_list:
        # id of net in netlist is id in csv - 1 ... fix
        net_id += 1
        starting_position: Position = circuit.get_net_start(netlist_id, net_id)

        # place first coordinate (of gate, so shouldn't count as wire!) 
        # shouldn't already be done somewhere else?
        circuit.lay_wire(netlist_id, net_id, starting_position[0], starting_position[1])

        # Make the wire connect to the last gate
        circuit = make_wire(circuit, netlist_id, net_id)

        print("-------DONE-------\n")
        print(circuit)
        break
        
