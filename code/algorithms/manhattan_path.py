from code.classes.circuit import Circuit
from code.classes.net import Net
from code.classes.gate import Gate
from code.classes.wire import Wire


def make_manhattan_connection(net: Net):
    gate1, gate2 = net.gates

    # Check which gate has a lower X value, start from there
    # Lay wires along the X direction
    if gate1.position[0] > gate2.position[0]:
        dx = gate1.position[0] - gate2.position[0]
        if dx > 0:
            for i in range(dx + 1):
                net.add_wire(Wire(gate1.position[0] - i, gate1.position[1], 0))
        
    else:
        dx = gate2.position[0] - gate1.position[0]
        if dx > 0:
            for i in range(dx + 1):
                net.add_wire(Wire(gate1.position[0] + i, gate1.position[1], 0))

    
    # Check which gate has a lower Y value, start from there
    # Lay wires along the Y direction
    if gate1.position[1] > gate2.position[1]:
        dy = gate1.position[1] - gate2.position[1]
        if dy > 0:
            for i in range(dy):
                net.add_wire(Wire(gate2.position[0], gate2.position[1] + i, 0))
    
    else:
        dy = gate2.position[1] - gate1.position[1]
        if dy > 0:
            for i in range(dy + 1):
                net.add_wire(Wire(gate2.position[0], gate2.position[1] - i, 0))
