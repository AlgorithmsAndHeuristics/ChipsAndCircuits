import os, sys, time
from stopit import threading_timeoutable as timeoutable

directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algorithms"))

from circuit import Circuit
from greedy import greedy_make_nets
from randomised_greedy import random_greedy_make_nets

@timeoutable()
def random_greedy_make_nets_timed(circuit, net_id):
    """
    PRE: circuit object, chip_id and netlist_id.
    POST: Runs random algorithm on the circuit returns bool indicating if the run was succesful.
    """

    succesful_circuit = random_greedy_make_nets(circuit, net_id)

    if not succesful_circuit:
         return False
    else:
         return True


if __name__ == "__main__":
    net_id = 1

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

    print("\nPlease select which algorithm you'd like to use.\n\
Enter 0 to use the greedy algorithm.\n\
Enter 1 to use the iterative greedy algorithm.\n")

    # Prompt for the algorithm specification
    while True:
        chosen_algorithm = int(input("> "))

        if chosen_algorithm in range(2):
            break        


    print("Would you like to run the algorithm in plot mode or experiment mode?\n\
Enter 0 for plot mode: The algorithm is run once and the resulting configuration gets presented in a plot.\n\
Enter 1 for experiment mode: The algorithm is run for the given duration \
and the cost gets written to experiments/main_costs.txt.\n")
    
    while True:
            chosen_mode = int(input("> "))

            if chosen_mode in range(2):
                break

    # Ask for a run count in case of experiment mode
    if chosen_mode == 1:
        plot = False
        write = True

        print("For how many seconds would you like to run the algorithm? Please enter a positive, whole number.")

        # Prompt for test count
        while True:
            total_time = int(input("> "))

            if type(total_time == int):
                break

        start_time_global = time.time()
        
        # Run for the specified duration
        while time.time() - start_time_global < total_time:
        
            start_time_local = time.time()
            
            circuit = Circuit(f"data/chip_{chip}/print_{chip}.csv")
            circuit.load_netlist(f"data/chip_{chip}/netlist_{netlist}.csv")


            # Run the greedy algorithm
            if chosen_algorithm == 0:
                greedy_make_nets(circuit, net_id)
                succesfull_circuit  = True

            # Run the iterative greedy algorithm
            else:
                succesfull_circuit = random_greedy_make_nets_timed(timeout = 60, circuit = circuit, net_id = net_id)     
        
            # Only write data to txt file if the algorithm found a solution
            if not succesfull_circuit:
                print("Failed to find a solution")
            
            else:
                # Print the configuration cost as a status report
                print(f"Configuration cost: {sum([netlist.get_cost() for netlist in circuit.netlists])}")

                with open('code/experiments/results/main_costs.txt', "a") as file:
                    cost = sum([netlist.get_cost() for netlist in circuit.netlists])
                    visited_states = sum([net.state_counter for net in circuit.netlists[0].nets.values()])
                    file.write(f'{cost},{time.time() - start_time_local},{visited_states}\n')

    # Run the chosen algorithm in plot mode
    else:
        start_time_local = time.time()
        circuit = Circuit(f"data/chip_{chip}/print_{chip}.csv")
        circuit.load_netlist(f"data/chip_{chip}/netlist_{netlist}.csv")

        print(chosen_algorithm)
        # Run the greedy algorithm
        if chosen_algorithm == 0:
            greedy_make_nets(circuit, net_id)
            succesful_circuit = True

        # Run the random greedy algorithm
        else:
            succesful_circuit = random_greedy_make_nets(circuit, net_id)         

        # Only return relevant data if the algorithm found a solution
        if not succesful_circuit:
            print("Failed to find a solution")
            
        else:
            # Print relevant data and plot the circuit
            print(f"Runtime: {time.time() - start_time_local}")
            print(f"States visited: {sum([net.state_counter for net in circuit.netlists[0].nets.values()])}")
        
        # Plot the grid
        circuit.plot_grid(f"Chip {chip}, Netlist {netlist}")