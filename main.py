import os, sys
import time
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algorithms"))

from circuit import Circuit
#from hill_climber import HillClimber
from state_pruner import make_nets


if __name__ == "__main__":

    print("Please select which chip you'd like to use.\n")
    for i in range(3): print(f"Enter {i} to use chip_{i}")

    # Prompt for the chip specification
    while True:
        chip = int(input("> "))

        if chip in range(3):
                break

    print(f"\nPlease select which netlist you'd like to use\n")
    for i in range(3): print(f"Enter {chip * 3 + i + 1} to use netlist_{chip * 3 + i + 1}")

    # Prompt for the netlist specification
    while True:
            netlist = int(input("> "))

            if netlist in range(chip * 3 + 1,  chip * 3 + 4):
                break

    print("Would you like to run the algorithm in plot mode or experiment mode?\n\
Enter 0 for plot mode: The algorithm is run once and the resulting configuration gets presented in a plot.\n\
Enter 1 for experiment mode: The algorithm is run a prompted number of times \
and the cost gets written to experiments/main_costs.txt.\n")
    
    while True:
            chosen_mode = int(input("> "))

            if chosen_mode in range(2):
                break

    # Ask for a run count in case of experiment mode
    if chosen_mode == 1:
        plot = False
        write = True

        print("How many times would you like to run the algorithm? Please enter a positive, whole number.")

        # Prompt for test count
        while True:
            run_count = int(input("> "))

            if type(run_count == int):
                break
    else:
        run_count = 1
        plot = True
        write = False

    use_hill_climber: bool = False
    net_id = 1


    for i in range(run_count):
    
        start_time_local = time.time()
        
        circuit = Circuit(f"data/chip_{chip}/print_{chip}.csv")


        circuit.load_netlist(f"data/chip_{chip}/netlist_{netlist}.csv")


        #for net in circuit.netlists[0].nets.values():
        #    print(f"Gate {net.gates[0]} to gate {net.gates[1]}")

        make_nets(circuit, net_id)


        #if use_hill_climber:
            #hill_climber: HillClimber = HillClimber(circuit)
            
        
        # Print the configuration cost as a status report
        print(f"Configuration cost: {sum([netlist.get_cost() for netlist in circuit.netlists])}")


        if plot:
            # Print relevant data and plot the circuit
            print(f"Runtime: {time.time() - start_time_local}")
            print(f"States visited: {sum([net.state_counter for net in circuit.netlists[0].nets.values()])}")

            circuit.plot_grid("Chip 0, Netlist 1")

        if write: 
            # Write the cost and excecution runtime to the file
            with open('code/experiments/results/main_costs.txt', "a") as file:
                    cost = sum([netlist.get_cost() for netlist in circuit.netlists])
                    visited_states = sum([net.state_counter for net in circuit.netlists[0].nets.values()])
                    file.write(f'{cost},{time.time() - start_time_local},{visited_states}\n')

