import os, sys
from stopit import threading_timeoutable as timeoutable

directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algorithms"))

from circuit import Circuit
from randomise import make_nets

# Attempt to lay the nets within the given time limit
# Adds the cost values to costs.txt
@timeoutable()
def make_net_timed(circuit, netlist_id, plot: bool = False):

    make_nets(circuit = circuit, netlist_id = net_id)

    print(f"Configuration cost: {sum([netlist.get_cost() for netlist in circuit.netlists])}")

    with open('code/experiments/baseline_costs.txt', "a") as fhandle:
            fhandle.write(f'{sum([netlist.get_cost() for netlist in circuit.netlists])}\n')

    if plot:
        print(f"Plotting grid:")
        return circuit.plot_grid("Chip 0, Netlist 1")


if __name__ == "__main__":
    for i in range(1):
        chip = 0
        net_id = 1
        circuit = Circuit(f"data/chip_{chip}/print_{chip}.csv")

        circuit.load_netlist(f"data/chip_{chip}/netlist_{net_id}.csv")


        print(f"Netlist 1 has {len(circuit.netlists[0].nets)} nets")
        print(f"A connection is required from gates:")

        for net in circuit.netlists[0].nets:
            print(f"Gate {net.gates[0]} to gate {net.gates[1]}")

        make_net_timed(timeout = 10, circuit = circuit, netlist_id = net_id, plot = True)
        
