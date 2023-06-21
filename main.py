import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algorithms"))

from circuit import Circuit
from hill_climber import HillClimber
from state_pruner import make_nets


if __name__ == "__main__":
    use_hill_climber: bool = False
    
    chip = 0
    net =  1
    net = (chip * 3) + net
    #NOTE PROBLEM OF CIRCUIT CLASS
    net_id = 1
    
    circuit = Circuit(f"data/chip_{chip}/print_{chip}.csv")


    circuit.load_netlist(f"data/chip_{chip}/netlist_{net}.csv")

    print(f"Netlist 1 has {len(circuit.netlists[0].nets)} nets")
    print(f"A connection is required from gates:")

    for net in circuit.netlists[0].nets:
        print(f"Gate {net.gates[0]} to gate {net.gates[1]}")

    make_nets(circuit, net_id)

    print(f"Configuration cost: {sum([netlist.get_cost() for netlist in circuit.netlists])}")

    # ----------
    
    if use_hill_climber:
        # Joey's algorithm
        hill_climber: HillClimber = HillClimber(circuit)
        
        # Just do 10 iterations (an arbitrary amount) for now
        for _ in range(10):
            hill_climber.make_incremental_change()
    
    # ----------
    
    print(f"Plotting grid:")


    circuit.plot_grid("Chip 0, Netlist 1")

