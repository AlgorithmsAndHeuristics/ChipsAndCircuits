import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algorithms"))

# Import used datastructures
from circuit import Circuit
from gate import Gate
from netlist import Netlist
from net import Net

if __name__ == "__main__":
    chip, netlist = 0, 1

    circ = Circuit(f"data/chip_{chip}/print_{chip}.csv", 3)

    print(f"Initial circuit:\n{circ}")

    circ.load_netlist(f"data/chip_{chip}/netlist_{netlist}.csv")

    print(f"Netlist {netlist} has {len(circ.netlists[0].nets)} nets")
    print(f"A connection is required from gates:")

    for net in circ.netlists[0].nets:
        print(f"Gate {net.gates[0]} to gate {net.gates[1]}")

    for wire in [(1,1)]:
        circ.netlists[0].nets[0].add_wire(wire[0], wire[1])
