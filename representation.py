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
from wire import Wire

if __name__ == "__main__":

    chip = 0
    net = (chip * 3) + 1
    circ = Circuit(f"data/chip_{chip}/print_{chip}.csv")

    print(f"Initial circuit:\n{circ}")

    circ.load_netlist(f"data/chip_{chip}/netlist_{net}.csv")

    print(f"Netlist 1 has {len(circ.netlists[0].nets)} nets")
    print(f"A connection is required from gates:")

    for net in circ.netlists[0].nets:
        print(f"Gate {net.gates[0]} to gate {net.gates[1]}")

    for d in [(5,2), (4,2), (3,2), (3,3), (2,3)]:
        wire = Wire(d[0], d[1])
        circ.netlists[0].nets[0].add_wire(wire)

    print(f"\nCircuit after adding a wire from gate 1 to gate 5:\n{circ}")

    print(f"Current cost: {circ.netlists[0].get_cost()}")

    for d in [(5,5), (5,4), (5,3), (5,2)]:
        wire = Wire(d[0], d[1])
        circ.netlists[0].nets[1].add_wire(wire)

    print(f"\nCircuit after adding a wire from gate 2 to gate 1:\n{circ}")

    print(f"Current cost: {circ.netlists[0].get_cost()}")

    print("-----------------------")

    print("Adding an enlargement factor increases the grid size")

    print(Circuit(f"data/chip_{chip}/print_{chip}.csv", 2))
    