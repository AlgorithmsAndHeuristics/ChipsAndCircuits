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

circ = Circuit("data/chip_0/print_0.csv")

print(f"Initial circuit:\n{circ.get_representation()}")

circ.load_netlist("data/chip_0/netlist_1.csv")

print(f"Netlist 1 has {len(circ.netlists[0].nets)} nets")
print(f"A connection is required from gates:")

for net in circ.netlists[0].nets:
    print(f"Gate {net.gates[0]} to gate {net.gates[1]}")

for wire in [(1,1)]:
    circ.netlists[0].nets[0].add_wire(wire[0], wire[1])

print(f"Initial circuit:\n{circ.get_representation()}")

