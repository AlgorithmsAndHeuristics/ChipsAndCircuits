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
    chip, netlist, enlarge_factor = 0, 1, 3

    circ = Circuit(f"data/chip_{chip}/print_{chip}.csv", enlarge_factor)

    print(f"Initial circuit:\n{circ}")

    circ.load_netlist(f"data/chip_{chip}/netlist_{netlist}.csv")

    print(f"Netlist {netlist} has {len(circ.netlists[0].nets)} nets")
    print(f"A connection is required from gates:")

    for net in circ.netlists[0].nets:
        print(f"Gate {net.gates[0]} to gate {net.gates[1]}")

for wire in [(5,2), (4,2), (3,2), (3,3), (2,3)]:
    circ.netlists[0].nets[0].add_wire(wire[0], wire[1])

print(f"\nCircuit after adding a wire from gate 1 to gate 5:\n{circ.get_representation()}")

print(f"Current cost: {circ.netlists[0].get_cost()}")

for wire in [(5,5), (5,4), (5,3), (5,2)]:
    circ.netlists[0].nets[1].add_wire(wire[0], wire[1])

print(f"\nCircuit after adding a wire from gate 2 to gate 1:\n{circ.get_representation()}")
