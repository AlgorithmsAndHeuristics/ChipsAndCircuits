import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algorithms"))

from circuit import Circuit
from randomise import make_nets


if __name__ == "__main__":
    chip = 0
    net_id = (chip * 3) + 1
    circuit = Circuit(f"data/chip_{chip}/print_{chip}.csv")

    print(f"Initial circuit:\n{circuit}")

    circuit.load_netlist(f"data/chip_{chip}/netlist_{net_id}.csv")

    print(f"Netlist 1 has {len(circuit.netlists[0].nets)} nets")
    print(f"A connection is required from gates:")

    for net in circuit.netlists[0].nets:
        print(f"Gate {net.gates[0]} to gate {net.gates[1]}")

    make_nets(circuit, net_id)