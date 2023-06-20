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

TODO:
Line can't enter now when a line under/above on either
start or end gate > endless loop
"""

from code.classes.circuit import Circuit


def correct_line(circuit: Circuit, netlist_id: int, net_id: int) -> Circuit:
    """
    Check if the straight line has no intersections. If it does,
    try to move a plane up first i.e. same line but
    first move up last move down. If another intersection is encountered,
    try to move a plane down. Loop this with adding a layer
    everytime until no intersections encountered.

    PRE: circuit of type Circuit, netlist_id and net_id of type int
    POST: circuit of type Circuit
    """

    direction: int = 1
    n_level: int = 1

    while True:
        print(f"NET: {circuit.get_net(netlist_id, net_id)}")

        # Check if no intersections
        if not circuit.any_intersections(netlist_id):
            print("\nNO INTERSECTIONS")
            break
        
        print(f"\nINTERSECTION, MOVING {n_level} LEVEL {direction}")
        # Move a level
        circuit.move_level(netlist_id, net_id, direction, n_level)

        # Go to next layer
        if direction == 1:
            direction = -1
        else:
            direction = 1
            n_level += 1

    return circuit


def make_nets(circuit: Circuit, netlist_id: int):
    """
    Go off all nets in netlist in order of distance between it's gates,
    make a straight line, and correct the line if necessary.

    PRE: circuit of type Circuit and netlist_id of type int
    POST: nets from netlist of circuit are connected
    """

    print("\n-------START-------")

    # Get list of net id's in order of distance between the gates.
    sorted_nets = circuit.list_shortest_distance(netlist_id)
    x = 0
    for net_id in sorted_nets:
        
        print(f"\nDOING: netlist_id={netlist_id} | net_id={net_id - 1}")
        # id of net in netlist is id in csv - 1 ... fix
        net_id += 1
        
        # Make a net following a straight line
        circuit.lay_shortest_line(netlist_id, net_id)

        # Lay the correct straight line
        circuit = correct_line(circuit, netlist_id, net_id)

        x += 1
        if x == 6:
            break
        